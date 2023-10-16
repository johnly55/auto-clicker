import tkinter as tk

from . import events
from action import Action


class GUI:
    """Graphical user interface."""
    root: tk.Tk = ...
    menu_bar: tk.Menu = ...
    holder_fr: tk.Frame = ...
    action_fr: tk.Frame = ...
    design_fr: tk.Frame = ...
    canvas: tk.Canvas = ...
    canvas_windows: list[tk.Frame] = ...
    canvas_zoom = [0]
    action_copy : tk.Widget = ...
    
    def __init__(self, title: str=None) -> None:
        """Initializes gui with a title."""
        title = title if title is not None else ""
        self.initialize(title)
        self.add_preset_actions()

    def add_preset_actions(self) -> None:
        """Add action options to the Action frame.
        
        Various actions like Click, Wait, etc. will be added to the list of 
        options inside the Action frame.
        """
        # Create the action_copy without packing it.
        # Holds draggable GUI copy of the active action.
        self.action_copy = tk.Button(self.holder_fr, text="", relief=tk.RAISED, bd=1)

        # Add click action.
        click_action = Action(Action.ActionType.CLICK)
        click_item = tk.Button(self.action_fr, text=click_action.action_name.upper(), relief=tk.RAISED, bd=1)

        click_item.bind('<B1-Motion>', 
                        lambda event: events.on_drag_action(event, self.root, self.action_copy))
        click_item.bind('<Button-1>', 
                        lambda event: events.on_left_click_action(event, click_item, self.root, self.action_copy))
        click_item.bind('<ButtonRelease-1>', 
                        lambda event: events.on_left_release_action(event, self.canvas, self.canvas_windows, self.action_copy))
        click_item.pack()

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
        
        # TODO Expand grid as user scrolls
        # Draw a grid
        GRID_WIDTH = 500
        GRID_HEIGHT = 500
        LINES_PER_GRID = 10

        for i in range(LINES_PER_GRID):
            # Horizontal Lines.
            x_start = 0
            x_end = GRID_WIDTH
            y_pos = GRID_HEIGHT / LINES_PER_GRID * i
            canvas.create_line(x_start, y_pos, x_end, y_pos, fill='black', width=1)

            # Vertical Lines.
            x_pos = GRID_WIDTH / LINES_PER_GRID * i
            y_start = 0
            y_end = GRID_HEIGHT
            canvas.create_line(x_pos, y_start, x_pos, y_end, fill='black', width=1)

        # Bind user actions to canvas.
        canvas.bind('<Button-1>', lambda event: events.on_left_click_canvas(event, self.canvas))
        canvas.bind('<B1-Motion>', lambda event: events.on_drag_canvas(event, self.canvas))
        canvas.bind('<MouseWheel>', lambda event: events.on_mouse_scroll_canvas(event, self.canvas, self.canvas_zoom))
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
        self.canvas_windows = []
