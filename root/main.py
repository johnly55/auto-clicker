"""Main module to start program.

Starts the GUI and deals with user inputs.
"""
import pyautogui
from pynput.mouse import Button, Controller

from gui.gui import GUI

APP_NAME = "John Ly's Auto Clicker"


def main():
    """Creates a GUI instance and run it"""
    gui = GUI(APP_NAME)
    gui.run()

if __name__ == '__main__':
    main()
