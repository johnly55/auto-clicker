"""Graphical User Interface.

GUI sets up the tkinter interface and initializes all action presets.
User can drag actions onto the canvas grid and set up automated events.

Requires tkinter to be installed.

Includes classes:
    GUI - Only needs to be instantiated, then call the run function.
"""
import tkinter as tk

from action import Action
from . import events


# TODO Open up a config window for actions.
# TODO Remove unnecessary comments split init into different functions for simplicity.
class GUI:
    """Graphical user interface."""
    root: tk.Tk = ...
    menu_bar: tk.Menu = ...
    holder_fr: tk.Frame = ...
    action_fr: tk.Frame = ...
    design_fr: tk.Frame = ...
    config_fr: tk.Frame = ...
    canvas: tk.Canvas = ...
    canvas_windows: list[tk.Frame] = ...
    canvas_zoom = [0]
    action_copy : tk.Widget = ...
    action_stack : list[tuple[tk.Widget, Action]] = ...

    def __init__(self, title: str=None) -> None:
        """Initializes gui with a title."""
        title = title if title is not None else ""
        self._initialize(title)
        self._add_preset_actions()

    def run(self) -> None:
        """Runs tkinter mainloop function."""
        self.root.mainloop()

    ACTION_FONT = ('Arial', 12)
    def _add_preset_actions(self) -> None:
        """Add action options to the Action frame.
        
        Various actions like Click, Wait, etc. will be added to the list of 
        options inside the Action frame.
        """
        # Create the action_copy without packing it.
        # Holds draggable GUI copy of the active action.
        self.action_copy = tk.Button(self.holder_fr, text="", relief=tk.RAISED, bd=1)

        # Add click action.
        click_action = Action(Action.ActionType.CLICK)
        click_item = tk.Button(self.action_fr, text=click_action.action_name.upper(), 
                               relief=tk.RAISED, bd=1, font=self.ACTION_FONT)

        click_item.bind('<B1-Motion>',
                        lambda event: events.on_drag_action(
                            event, self.root, self.action_copy)
                            )
        click_item.bind('<Button-1>',
                        lambda event: events.on_left_click_action(
                            event, click_item, self.root, self.action_copy, self.canvas_zoom)
                            )
        click_item.bind('<ButtonRelease-1>',
                        lambda event: events.on_left_release_action(
                            event, self.canvas, self.canvas_windows, self.action_copy)
                            )
        click_item.pack()

    LABEL_FONT = ('Arial', 14)
    SIZE_HEIGHT = 600
    ACTION_MIN_WIDTH = 200
    CONFIG_MIN_WIDTH = 300
    def _initialize(self, title: str) -> None:
        """Initializes the gui.

        Creates the main Root window containing the Menu Bar,
        Action frame, and Design frame. Then sets the Root,
        the Actions frame to add more options to, and the Design frame
        to contain the actions and their configurations.
        
        Args:
            title: The window title.
        """
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
        action_label = tk.Label(action_fr, text='Actions',
                                font=self.LABEL_FONT, relief=tk.RIDGE, bd=2)
        action_label.pack(fill=tk.X)

        # Design holds actions and their configurations.
        design_fr = tk.Frame(holder_fr, relief=tk.GROOVE, bd=2)
        design_label = tk.Label(design_fr, text='Design',
                                font=self.LABEL_FONT, relief=tk.RIDGE, bd=2)
        design_label.pack(fill=tk.X)

        config_fr = tk.Frame(root, relief=tk.GROOVE, bd=2)
        config_label = tk.Label(config_fr, font=self.LABEL_FONT, text="Config",
                                relief=tk.RIDGE, bd=2)
        config_label.pack(fill=tk.X)

        # Canvas where actions can be dragged to.
        canvas = tk.Canvas(design_fr)

        self._draw_grid(canvas)
        canvas.config(scrollregion=canvas.bbox('grid'))

        # Bind user actions to canvas.
        canvas.bind('<Button-1>', lambda event: canvas.scan_mark(event.x, event.y))
        canvas.bind('<B1-Motion>', lambda event: canvas.scan_dragto(event.x, event.y, gain=1))
        canvas.bind('<MouseWheel>',
                    lambda event: events.on_mouse_scroll_canvas(
                        event, self.canvas, self.canvas_zoom, self.canvas_windows, self.ACTION_FONT)
                        )

        canvas.pack(fill=tk.BOTH, expand=True)

        action_fr.grid(row=0, column=0, sticky='news')
        design_fr.grid(row=0, column=1, sticky='news')

        # Disallow action_fr from expanding horizontally when window resizes.
        holder_fr.columnconfigure(0, weight=0, minsize=self.ACTION_MIN_WIDTH)
        # Allows resizing for design_fr both vertically and horizontally.
        holder_fr.rowconfigure(0, weight=1, minsize=self.SIZE_HEIGHT)
        holder_fr.columnconfigure(1, weight=1)

        holder_fr.grid(row=0, column=0, sticky="news")
        config_fr.grid(row=0, column=1, sticky="news")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=0, minsize=self.CONFIG_MIN_WIDTH)
        root.config(menu=menu_bar)

        self.root = root
        self.menu_bar = menu_bar
        self.holder_fr = holder_fr
        self.action_fr = action_fr
        self.design_fr = design_fr
        self.config_fr = config_fr
        self.canvas = canvas
        self.canvas_windows = []

    GRID_WIDTH = 500
    GRID_HEIGHT = 500
    LINES_PER_GRID = 10
    NUM_GRIDS_HORIZONTAL = 4
    NUM_GRIDS_VERTICAL = 4
    def _draw_grid(self, canvas: tk.Canvas):
        """Draws grids on the canvas.
        
        Draws vertical and horizontal lines inside of canvas.

        Args:
            canvas: Tk.canvas to draw grid in.
        """
        for grid_horizontal in range(self.NUM_GRIDS_HORIZONTAL):
            grid_horizontal -= self.NUM_GRIDS_HORIZONTAL // 2
            for grid_vertical in range(self.NUM_GRIDS_VERTICAL):
                grid_vertical -= self.NUM_GRIDS_VERTICAL // 2
                for i in range(self.LINES_PER_GRID):
                    # Horizontal Lines.
                    x_start = grid_horizontal * self.GRID_WIDTH
                    x_end = x_start + self.GRID_WIDTH
                    y_pos = self.GRID_HEIGHT / self.LINES_PER_GRID * i
                    y_pos += grid_vertical * self.GRID_HEIGHT
                    canvas.create_line(x_start, y_pos, x_end, y_pos,
                                       fill='black', width=1, tags='grid')

                    # Vertical Lines.
                    x_pos = self.GRID_WIDTH / self.LINES_PER_GRID * i
                    x_pos += grid_horizontal * self.GRID_WIDTH
                    y_start = grid_vertical * self.GRID_HEIGHT
                    y_end = y_start + self.GRID_HEIGHT
                    canvas.create_line(x_pos, y_start, x_pos, y_end,
                                       fill='black', width=1, tags='grid')
