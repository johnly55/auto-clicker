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
#TODO Zoom the canvas_window as well.
def on_mouse_scroll_canvas(event: tk.Event, canvas: tk.Canvas, canvas_zoom: list) -> None:
    """Zooms in/out the canvas.
    
    Depending on which way the mouse wheel scrolls, zoom in
    or out a certain amount before hitting a limit.

    Args:
        event: Tkinter event.
        canvas: Tkinter canvas to be zooming in/out on.
        canvas_zoom: Counter to track zooms in a certain direction.
    """
    gain = 0.06  # Speed of zoom.
    if event.delta > 0:
        if canvas_zoom[0] < ZOOM_LIMIT:
            canvas_zoom[0] += 1
            canvas.scale('all', event.x, event.y, 1 + gain, 1 + gain)
    else:
        if canvas_zoom[0] > -ZOOM_LIMIT:
            canvas_zoom[0] -= 1
            canvas.scale('all', event.x, event.y, 1 - gain, 1 - gain)

def on_drag_action(event: tk.Event, parent: tk.Widget, action_copy: tk.Widget, widget: tk.Widget=None) -> None:
        """Drags copy of an action to mouse position.
        
        Takes the saved copy of an action and drag it to where the mouse is.

        Args:
            event: Tkinter event.
            parent: Used as a position reference.
            action_copy: The tkinter widget that will be dragged.
            widget: The tkinter widget to grab height and width from.
        """
        mouse_pos = (event.x_root, event.y_root)
        parent_root_pos = (parent.winfo_rootx(), parent.winfo_rooty())

        if widget is None:
            offset = (action_copy.winfo_width() // 2, action_copy.winfo_height() // 2)
        else:
            # Widget doesn't start with proper offset unless the original widget is passed.
            # Ex: Mouse position is lop-left of the widget instead of the middle.
            offset = (widget.winfo_width() // 2, widget.winfo_height() // 2)
        
        local_x, local_y = _get_local_position(mouse_pos, parent_root_pos, offset)
        action_copy.place(x=local_x, y=local_y)

def on_left_click_action(event: tk.Event, widget: tk.Widget, parent: tk.Widget, action_copy: tk.Widget) -> None:
        """Create a copy of an action.
        
        Take a widget and create a copy of that, then drag it to where the mouse is.
        Take the class name of a given widget, collect all configurations and pass
        them to the constructor to create a copy of the widget.

        Args:
            event: Tkinter event.
            widget: The tkinter widget to clone.
            parent: Tkinter frame where the action_copy will be copied to.
            action_copy: Will copy the selected widget and move to the middle of the mouse.
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
    """Place action into design or delete.
    
    If the mouse is within the Canvas, place the dragged action item into it.
    Otherwise, delete it.

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
        canvas_window = tk.Frame()

        mouse_pos = (event.x_root, event.y_root)
        # canvasx and canvasy keeps the position correct when dragging throught the canvas.
        parent_root_pos = (canvas.winfo_rootx() - canvas.canvasx(0),
                           canvas.winfo_rooty() - canvas.canvasy(0))
        offset = (0, 0)
        
        local_x, local_y = _get_local_position(mouse_pos, parent_root_pos, offset)
        canvas.create_window(local_x, local_y, window=canvas_window, tags='canvas_window', 
                             width=action_copy.winfo_width(), height=action_copy.winfo_height())

        # Drags the canvas window to where the mouse is positioned

        canvas_copy = _get_clone_widget(action_copy, canvas_window)
        canvas_copy.pack()

    action_copy.place_forget()

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

def _get_local_position(mouse_pos: (int, int), parent_root_pos: (int, int), offset: (int, int)) -> (int, int):
     local_x = mouse_pos[0] - parent_root_pos[0] - offset[0]
     local_y = mouse_pos[1] - parent_root_pos[1] - offset[1]
     return (local_x, local_y)
