import tkinter as tk

from action import Action


class GUI:
    """Graphical user interface."""
    root: tk.Tk = ...
    menu_bar: tk.Menu = ...
    holder_fr: tk.Frame = ...
    action_fr: tk.Frame = ...
    design_fr: tk.Frame = ...
    canvas: tk.Canvas = ...
    canvas_window: tk.Frame = ...
    action_copy : tk.Widget = ...
    
    def __init__(self, title: str=None) -> None:
        """Initializes gui with a title."""
        title = title if title is not None else ""
        self.initialize(title)
        self.add_preset_actions()
        self.action_copy = None  # Holds draggable GUI copy of the active action.

    def add_preset_actions(self) -> None:
        """Add action options to the Action frame.
        
        Various actions like Click, Wait, etc. will be added to the list of 
        options inside the Action frame.
        """
        # Add click action.
        click_action = Action(Action.ActionType.CLICK)
        click_item = tk.Button(self.action_fr, text=click_action.action_name.upper(), relief=tk.RAISED, bd=1)
        click_item.bind('<B1-Motion>', lambda event: self.on_drag_action(event))
        click_item.bind('<Button-1>', lambda event: self.on_left_click_action(event, click_item))
        click_item.bind('<ButtonRelease-1>', lambda event: self.on_left_release_action(event))
        click_item.pack()

    def is_mouse_within_frame(self, frame: tk.Widget, mouse_x: int, mouse_y: int) -> bool:
        """Return is the mouse within the frame.
        
        If the mouse is within the given frame, return True, otherwise False.

        Args:
            frame: The frame to compare mouse position to.
            mouse_x: The absolute x position of the mouse.
            mouse_y: The absolute y position of the mouse.

        Returns:
            Boolean of whether the mouse is inside the frame or not.
        """
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()

        frame_left = frame.winfo_rootx()
        frame_top = frame.winfo_rooty()
        frame_bottom = frame_top + frame_height
        frame_right = frame_left + frame_width

        if (mouse_x >= frame_left and mouse_x <= frame_right and 
                mouse_y >= frame_top and mouse_y <= frame_bottom):
            return True
        return False

    def on_left_click_canvas(self, event: tk.Event) -> None:
        """Calls canvas' scan_mark function
        
        This function saves the mouse's position to be later used with
        the scan_dragto function.
        
        Args:
            event: Tkinter event.
        """
        self.canvas.scan_mark(event.x, event.y)

    def on_drag_canvas(self, event: tk.Event) -> None:
        """Calls canvas' scan_dragto function
        
        Using the mouse position saved with scan_mark, 
        simulate the canvas being dragged around.
        
        Args:
            event: Tkinter event.
        """
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def on_drag_action(self, event: tk.Event, widget: tk.Widget=None) -> None:
        """Drags copy of an action to mouse position.
        
        Takes the saved copy of an action and drag it to where the mouse is.

        Args:
            event: Tkinter event.
            widget: The tkinter widget to grab height and width from.
        """
        mouse_x, mouse_y = event.x_root, event.y_root
        chart_fr_x, chart_fr_y = self.holder_fr.winfo_rootx(), self.holder_fr.winfo_rooty()

        if widget is None:
            offset_x, offset_y = self.action_copy.winfo_width() // 2, self.action_copy.winfo_height() // 2
        else:
            # Widget doesn't start with proper offset unless the original widget is passed.
            # Ex: Mouse position is lop-left of the widget instead of the middle.
            offset_x, offset_y = widget.winfo_width() // 2, widget.winfo_height() // 2
        
        local_x = mouse_x - chart_fr_x - offset_x
        local_y = mouse_y - chart_fr_y - offset_y

        self.action_copy.place(x=local_x, y=local_y)

    def on_left_click_action(self, event: tk.Event, widget: tk.Widget) -> None:
        """Create a copy of an action.
        
        Take a widget and create a copy of that, then drag it to where the mouse is.
        Take the class name of a given widget, collect all configurations and pass
        them to the constructor to create a copy of the widget.

        Args:
            event: Tkinter event.
            widget: The tkinter widget to clone.
        """
        self.action_copy = self._get_clone_widget(widget, self.root)
        self.action_copy.pack()

        # Set starting position of the copy to the mouse position.
        self.on_drag_action(event, widget)

    def on_left_release_action(self, event: tk.Event) -> None:
        """Place action into design or delete.
        
        If the mouse is within the Canvas, place the dragged action item into it.
        Otherwise, delete it.

        Args:
            event: Tkinter event.
        """
        is_within = self.is_mouse_within_frame(self.canvas, event.x_root, event.y_root)
        
        if is_within:
            canvas_copy = self._get_clone_widget(self.action_copy, self.canvas_window)
            canvas_copy.pack()

        self.action_copy.destroy()
        self.action_copy = None

    def _get_clone_widget(self, widget: tk.Widget, parent: tk.Widget) -> tk.Widget:
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

    def initialize(self, title: str) -> None:
        """Initializes the gui.

        Creates the main Root window containing the Menu Bar,
        Action frame, and Design frame. Then sets the Root,
        the Actions frame to add more options to, and the Design frame
        to contain the actions and their configurations.
        
        Args:
            title: The window title.
        """
        LABEL_FONT = 'Arial 14'
        SIZE_HEIGHT = 600
        ACTION_MIN_WIDTH = 200

        root = tk.Tk()
        root.title(title)

        # Menu contains File, Edit, etc...
        menu_bar = tk.Menu(root)

        # TODO Add functionality to menu.
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Open')
        file_menu.add_command(label='Save')
        file_menu.add_command(label='Save As...')
        menu_bar.add_cascade(label='File', menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label='Undo')
        edit_menu.add_command(label='Redo')
        edit_menu.add_separator()
        edit_menu.add_command(label='Cut')
        edit_menu.add_command(label='Copy')
        edit_menu.add_command(label='Paste')
        menu_bar.add_cascade(label='Edit', menu=edit_menu)

        # Container to hold Action and Design frames.
        holder_fr = tk.Frame(root)

        # Actions has dragable options to do things with keyboard and/or mouse.
        action_fr = tk.Frame(holder_fr, relief=tk.GROOVE, bd=2)
        action_label = tk.Label(action_fr, text='Actions', font=LABEL_FONT, relief=tk.RIDGE, bd=2)
        action_label.pack(fill=tk.X)

        # Design holds actions and their configurations.
        design_fr = tk.Frame(holder_fr, relief=tk.GROOVE, bd=2)
        design_label = tk.Label(design_fr, text='Design', font=LABEL_FONT, relief=tk.RIDGE, bd=2)
        design_label.pack(fill=tk.X)

        # Canvas where actions can be dragged to.
        canvas = tk.Canvas(design_fr)

        # TODO Implement or delete
        # bbox = canvas.bbox('all')
        # canvas.config(scrollregion=bbox)
        canvas.create_rectangle(0,0,200,300,fill='red')

        # This frame exists within the canvas, and is dragged with it.
        canvas_window = tk.Frame()
        canvas.create_window(100, 100, window=canvas_window, anchor=tk.N)
        tk.Label(canvas_window, text="TEST").pack()

        canvas.bind('<Button-1>', self.on_left_click_canvas)
        canvas.bind('<B1-Motion>', self.on_drag_canvas)
        canvas.pack(fill=tk.BOTH, expand=True)

        action_fr.grid(row=0, column=0, sticky='news')
        design_fr.grid(row=0, column=1, sticky='news')

        # Disallow action_fr from expanding horizontally when window resizes.
        holder_fr.columnconfigure(0, weight=0, minsize=ACTION_MIN_WIDTH)
        # Allows resizing for design_fr both vertically and horizontally.
        holder_fr.rowconfigure(0, weight=1, minsize=SIZE_HEIGHT)
        holder_fr.columnconfigure(1, weight=1)
        holder_fr.pack(fill=tk.BOTH, expand=True)

        root.config(menu=menu_bar)

        self.root = root
        self.menu_bar = menu_bar
        self.holder_fr = holder_fr
        self.action_fr = action_fr
        self.design_fr = design_fr
        self.canvas = canvas
        self.canvas_window = canvas_window
