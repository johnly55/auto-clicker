import tkinter as tk


def on_left_click_canvas(event: tk.Event, canvas: tk.Canvas) -> None:
    """Canvas saves mouse position.
    
    This function saves the mouse's position to be later used with
    the scan_dragto function.
    
    Args:
        event: Tkinter event.
        canvas: Tkinter canvas to scan and drag through.
    """
    canvas.scan_mark(event.x, event.y)

def on_drag_canvas(event: tk.Event, canvas: tk.Canvas) -> None:
        """Drag canvas when mouse moves.
        
        Using the mouse position saved with scan_mark, simulate
        the canvas being dragged around with the scan_dragto function.
        
        Args:
            event: Tkinter event.
            canvas: Tkinter canvas to scan and drag through.
        """
        canvas.scan_dragto(event.x, event.y, gain=1)

ZOOM_LIMIT = 5
def on_mouse_scroll_canvas(event: tk.Event, canvas: tk.Canvas, canvas_zoom: list, 
                           canvas_windows: list[tk.Frame], font: (str, int)) -> None:
    """Zooms in/out the canvas.
    
    Depending on which way the mouse wheel scrolls, zoom in
    or out a certain amount before hitting a limit.
    Also, slightly increase/decrease of font size of actions in canvas.

    Args:
        event: Tkinter event.
        canvas: Tkinter canvas to be zooming in/out on.
        canvas_zoom: Counter to track the amount zooms in a certain direction.
        canvas_windows: List of canvas windows, each containing an action.
        font: The default font of the action to change size of.
    """
    gain = 0.06  # Speed of zoom.
    did_zoom = False
    if event.delta > 0:
        if canvas_zoom[0] < ZOOM_LIMIT:
            canvas_zoom[0] += 1
            scale = 1 + gain
            canvas.scale('all', 0, 0, scale, scale)
            did_zoom = True
    else:
        if canvas_zoom[0] > -ZOOM_LIMIT:
            canvas_zoom[0] -= 1
            scale = 1 / (1 + gain)
            canvas.scale('all', 0, 0, scale, scale)
            did_zoom = True

    if did_zoom:
        return
        # TODO Redraw the window to fit font size
        # If we zoomed in or out, adjust the font size accordingly.
        for canvas_window in canvas_windows:
                action = canvas_window.winfo_children()[0]
                font = (font[0], font[1] + canvas_zoom[0])
                action.config(font=font)
                width = action.cget('width')
                height = action.cget('height')
                # Resize and redraw.
                canvas_window.config(width=width, height=height)
                x = (canvas_window.winfo_x() - canvas.canvasx(0))
                y = (canvas_window.winfo_y() - canvas.canvasy(0))
                local_x = x
                local_y = y
                canvas.create_window(local_x, local_y, window=canvas_window, tags='canvas_window', 
                             width=width, height=height)


def on_drag_action(event: tk.Event, parent: tk.Widget, drag_widget: tk.Widget, reference_widget: tk.Widget=None) -> None:
        """Drags copy of a widget to the mouse position.
        
        The widget is dragged to the mouse position based on the parent's relative
        position, the mouse position, and an offset.

        Args:
            event: Tkinter event.
            parent: Used as a position reference.
            drag_widget: The tkinter widget that will be dragged.
            reference_widget: The tkinter widget to grab height and width from to set offset.
        """
        mouse_pos = (event.x_root, event.y_root)
        parent_root_pos = (parent.winfo_rootx(), parent.winfo_rooty())

        if reference_widget is None:
            offset = (drag_widget.winfo_width() // 2, drag_widget.winfo_height() // 2)
        else:
            # Widget doesn't start with proper offset unless the original widget is passed.
            # Ex: Mouse position is lop-left of the widget instead of the middle.
            offset = (reference_widget.winfo_width() // 2, reference_widget.winfo_height() // 2)
        
        local_x, local_y = _get_local_position(mouse_pos, parent_root_pos, offset)
        drag_widget.place(x=local_x, y=local_y)

def on_left_click_action(event: tk.Event, widget: tk.Widget, parent: tk.Widget, action_copy: tk.Widget) -> None:
        """Create a copy of an action.
        
        Take a widget and create a copy of that, then drag it to where the mouse is.
        Copy the text, height, and width.

        Args:
            event: Tkinter event.
            widget: The tkinter widget to clone.
            parent: Tkinter frame where the action_copy will be copied to.
            action_copy: Will copy the selected widget and move to the mouse.
        """
        # Copy size and text of the widget.
        action_copy.configure(
             text=widget.cget('text'),
             width=widget.cget('width'),
             height=widget.cget('height')
             )
        action_copy.grid()

        # Set starting position of the copy to the mouse position.
        on_drag_action(event, parent, action_copy, widget)

def on_left_release_action(event: tk.Event, canvas: tk.Canvas, canvas_windows: list[tk.Frame], action_copy: tk.Widget) -> None:
    """Place copy of action in canvas if hovering over it.
    
    If the mouse is within the Canvas, create a canvas_window and 
    copy the dragged action item into it. Otherwise, delete it.

    Args:
        event: Tkinter event.
        canvas: Tkinter canvas to check if mouse is hovering over.
        canvas_windows: Append a new canvas window to this list to keep track of actions.
        action_copy: Widget will be cloned and added to canvas_window.
    """
    is_within = _is_mouse_within_frame(canvas, (event.x_root, event.y_root))
    
    if is_within:
        # TODO Look into tag_bind later on for arrows. #canvas.tag_bind('canvas_window', '<Enter>', lambda event: print(event))
        # Create a canvas_window at the mouse position for each action dragged to canvas.
        # This frame exists within the canvas, and is dragged with it.
        canvas_window = tk.Frame(canvas)

        mouse_pos = (event.x_root, event.y_root)
        # canvasx and canvasy helps keep the position correct when dragging throught the canvas.
        parent_root_pos = (canvas.winfo_rootx() - canvas.canvasx(0),
                           canvas.winfo_rooty() - canvas.canvasy(0))
        local_x, local_y = _get_local_position(mouse_pos, parent_root_pos)
        canvas.create_window(local_x, local_y, window=canvas_window, tags='canvas_window', 
                             width=action_copy.winfo_width(), height=action_copy.winfo_height())

        # Copy and pack the action into this canvas_window.
        canvas_copy = _get_clone_widget(action_copy, canvas_window)
        canvas_copy.bind('<B1-Motion>', lambda event: on_drag_action(event, canvas, canvas_window))
        canvas_copy.bind('<ButtonRelease-1>', lambda event: on_release_action_in_canvas(event, canvas, canvas_window))
        canvas_copy.pack()
        canvas_windows.append(canvas_window)

    # Make the action_copy invisible when not in use.
    action_copy.place_forget()

def on_release_action_in_canvas(event: tk.Event, canvas: tk.Widget, canvas_window: tk.Widget) -> None:
        """Redraws the action on the canvas.
        
        Redraw the canvas_window in the canvas when it stops being dragged.
        This provides a cleaner animation than placing on drag.

        Args:
            event: Tkinter event.
            canvas: Used as a position reference.
            canvas_window: The tkinter widget that will be dragged.
        """
        # The place() and create_window() functions work differently in the canvas.
        mouse_pos = (event.x_root, event.y_root)
        # canvasx and canvasy helps keep the position correct when dragging throught the canvas.
        parent_root_pos = (canvas.winfo_rootx() - canvas.canvasx(0),
                           canvas.winfo_rooty() - canvas.canvasy(0))
        local_x, local_y = _get_local_position(mouse_pos, parent_root_pos)
        canvas.create_window(local_x, local_y, window=canvas_window, tags='canvas_window', 
                             width=canvas_window.winfo_width(), height=canvas_window.winfo_height())

def _is_mouse_within_frame(frame: tk.Widget, mouse_pos: (int, int)) -> bool:
    """Return is the mouse within the frame.
    
    If the mouse is within the given frame, return True, otherwise False.

    Args:
        frame: The frame to compare mouse position to.
        mouse_pos: The absolute position of the mouse as a tuple (x, y).

    Returns:
        Boolean of whether the mouse is inside the frame or not.
    """
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()

    frame_left = frame.winfo_rootx()
    frame_top = frame.winfo_rooty()
    frame_bottom = frame_top + frame_height
    frame_right = frame_left + frame_width

    if (mouse_pos[0] >= frame_left and mouse_pos[0] <= frame_right and 
            mouse_pos[1] >= frame_top and mouse_pos[1] <= frame_bottom):
        return True
    return False



def _get_clone_widget(widget: tk.Widget, parent: tk.Widget) -> tk.Widget:
    """Returns a clone of a widget.
    
    The widget's __class__ is used to create an instance of the widget using
    attributes retrieved from the widget's cget function.

    Args:
        widget: The thing to clone.
        parent: Set the widget's master variable to.

    Returns:
        A clone of the widget not connected through reference.
    """
    cls = widget.__class__                                       # Class name.
    cfg = {key: widget.cget(key) for key in widget.configure()}  # Configuration settings.
    return cls(parent, **cfg)

def _get_local_position(mouse_pos: (int, int), parent_root_pos: (int, int), offset: (int, int)=(0, 0)) -> (int, int):
     """Returns the local position of the mouse.
     
     Calculate the relative position of the mouse in the parent window using the mouse position,
     the root position of the parent window, and a offset.

     Args:
        mouse_pos: Tuple containing the x and y position of the mouse.
        parent_root_pos: Tuple containing the x and y position of the top-left window.
        offset: Tuple to offset the local x and y position.

    Returns:
        The tuple of the local x and y position of the mouse inside the parent window.
     """
     local_x = mouse_pos[0] - parent_root_pos[0] - offset[0]
     local_y = mouse_pos[1] - parent_root_pos[1] - offset[1]
     return (local_x, local_y)
