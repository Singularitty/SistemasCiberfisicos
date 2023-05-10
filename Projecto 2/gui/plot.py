from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import axes
import matplotlib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import numpy as np
import layout
import thread
import socket
import threading

HOST = ""  # The server's hostname or IP address
PORT = 5555  # The port used by the server

class Plot():
    """
    Class representing a plot with temperature information.

    Attributes:
        soc (socket.socket): Socket object for communication with the server.
        window (sg.Window): PySimpleGUI window object.
        my_thread (thread.ThreadClass): Custom thread object for updating the plot.
    """

    soc:socket.socket
    window:sg.Window
    my_thread:thread.ThreadClass

    def __init__(self) -> None:
        """
            Initializes the Plot class.

            This class handles the creation of plots and the communication with a server.

            Args:
                None

            Returns:
                None
        """
        self.window = layout.create_window()
        # Add the plot to the window
        in_temp_fig_canvas = self.create_temps_figure(self.window["-TEMP_PLOT-"].TKCanvas)
        heat_fig_canvas = self.create_figure(self.window["-RES_PLOT-"].TKCanvas)
        fan_fig_canvas = self.create_figure(self.window["-FAN_PLOT-"].TKCanvas)
        fig_canvas = (in_temp_fig_canvas, heat_fig_canvas, fan_fig_canvas)
        #initialize thread
        self.my_thread = thread.ThreadClass(self.window, fig_canvas)
        self.my_thread.start()
        #self.soc = self.create_socket(HOST, PORT) #TODO

    def create_socket(self, HOST:str, PORT:int) -> socket:
        """
            Creates and connects a socket to a specified host and port.

            Args:
                HOST (str): The hostname or IP address of the server.
                PORT (int): The port number.

            Returns:
                socket: The created socket object.
        """
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((HOST, PORT))
        return soc
    
    def create_temps_figure(self, canvas) -> FigureCanvasTkAgg:
        """
            Creates and displays a temperature figure on a Tkinter canvas.

            Args:
                canvas: The Tkinter canvas object.

            Returns:
                FigureCanvasTkAgg: The created figure canvas.
        """
        fig:plt.Figure = plt.Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        ax:axes.Axes = fig.add_subplot(111)
        ax.plot(t, 2 * np.sin(2 * np.pi * t), label='in_temp')
        ax.plot(t, 2 * np.sin(2 * np.pi * t)*4, label='out_temp')
        ax.axhline(y=0, color='r', linestyle='-')
        ax.axhline(y=0, color='r', linestyle='-')
        ax.legend()

        matplotlib.use("TkAgg")
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg
    
    def create_figure(self, canvas):
        """
            Creates and displays a figure on a Tkinter canvas.

            Args:
                canvas: The Tkinter canvas object.

            Returns:
                FigureCanvasTkAgg: The created figure canvas.
        """
        fig:plt.Figure = plt.Figure(figsize=(3, 2), dpi=100)
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot(111)
        ax.plot(t, 2 * np.sin(2 * np.pi * t))

        matplotlib.use("TkAgg")
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg
    
    def send_temp_info(self, info:str) -> None:
        """
            Sends temperature information to the server.

            Args:
                info (str): Temperature information to send.

            Returns:
                None
        """
        self.soc.sendall(info)

    def update_state(self, temp:str, temp_int:str) -> None:
        """
            Updates the state display with temperature and interval information.

            Args:
                temp (str): Temperature value.
                temp_int (str): Temperature interval value.

            Returns:
                None
        """
        to_state = "Temp: " + temp + "ºC and Interval: " + temp_int + "ºC"
        self.window["-C_STATE-"].update(to_state)
        
    def kill_thread(self) -> None:
        """
            Stops the thread execution.

            Args:
                None

            Returns:
                None
        """
        self.my_thread.kill()

