from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import numpy as np
import layout
import thread
import socket

HOST = ""  # The server's hostname or IP address
PORT = 5555  # The port used by the server

class Plot():

    soc:socket.socket
    window:sg.Window
    my_thread:thread.ThreadClass

    def __init__(self) -> None:
        self.window = layout.create_window()
        self.my_thread = thread.ThreadClass(self.window)
        self.my_thread.start()
        #self.soc = self.create_socket(HOST, PORT)

    def create_socket(self, HOST:str, PORT:int) -> socket:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((HOST, PORT))
        return soc
    
    def update_figure(self, canvas):
        fig:plt.Figure = plt.Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        matplotlib.use("TkAgg")
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg
    
    def send_temp_info(self, info:str) -> None:
        self.soc.sendall(info)

    def update_state(self, temp:str, temp_int:str) -> None:
        to_state = "Temp: " + temp + "ºC and Interval: " + temp_int + "ºC"
        self.window["-C_STATE-"].update(to_state)

    def kill_thread(self) -> None:
        self.my_thread.kill()

