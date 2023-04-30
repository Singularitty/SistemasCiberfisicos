import threading
import PySimpleGUI as sg

class ThreadClass(threading.Thread):
    window:sg.Window
    is_killed:bool

    def __init__(self, window:sg.Window) -> None:
        threading.Thread.__init__(self)
        self.window = window
        self.is_killed = False

    def run(self) -> None:
        while not self.is_killed:
            # receive info from socket and update plot
            pass
    def kill(self) -> None:
        self.is_killed = True

