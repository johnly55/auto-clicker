import tkinter as tk


class GUI:
    def __init__(self, title: str=None):
        title = title if title is not None else ""
        self.initialize(title)

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
        DESIGN_MIN_WIDTH = 600
        ACTION_MIN_WIDTH = 200

        root = tk.Tk()
        root.title(title)

        # Menu contains File, Edit, etc...
        menu_bar = tk.Menu(root)

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

        # Actions has dragable options to do things with keyboard and/or mouse.
        action_fr = tk.Frame(root, relief=tk.GROOVE, bd=2)
        action_label = tk.Label(action_fr, text='Actions', font=LABEL_FONT, relief=tk.RIDGE, bd=2)
        action_label.pack(fill=tk.X)

        # Design holds actions and their configurations.
        design_fr = tk.Frame(root, relief=tk.GROOVE, bd=2)
        design_label = tk.Label(design_fr, text='Design', font=LABEL_FONT, relief=tk.RIDGE, bd=2)
        design_label.pack(fill=tk.X)

        action_fr.grid(row=0, column=0, sticky='news')
        design_fr.grid(row=0, column=1, sticky='news')

        # Disallow action_fr from expanding horizontally when window resizes.
        root.columnconfigure(0, weight=0, minsize=ACTION_MIN_WIDTH)

        # Allows resizing for design_fr both vertically and horizontally.
        root.rowconfigure(0, weight=1, minsize=SIZE_HEIGHT)
        root.columnconfigure(1, weight=1, min=DESIGN_MIN_WIDTH)

        root.config(menu=menu_bar)

        self.root = root
        self.menu_bar = menu_bar
        self.action_fr = action_fr
        self.design_fr = design_fr