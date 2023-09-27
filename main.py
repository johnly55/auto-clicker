import tkinter as tk
import pyautogui
from pynput.mouse import Button, Controller 

APP_NAME = "John Ly's Auto Clicker"


def main():
    root = tk.Tk()
    root.title("John Ly's Auto Clicker")

    menu_bar_fr = tk.Frame(root)
    actions_fr = tk.Frame(root)
    design_fr = tk.Frame(root)

    menu_bar_fr.grid(row=0, column=0)
    actions_fr.grid(row=1, column=0)
    design_fr.grid(row=1, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()