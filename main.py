import tkinter as tk
import pyautogui
from pynput.mouse import Button, Controller

from gui import GUI

APP_NAME = "John Ly's Auto Clicker"


def main():
    gui = GUI(APP_NAME)
    gui.root.mainloop()

if __name__ == '__main__':
    main()
