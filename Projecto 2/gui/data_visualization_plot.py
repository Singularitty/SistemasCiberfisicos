# System Imports
import socket
import threading
import matplotlib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import axes

# Data Visualization Components
import data_visualization_layout as layout
import data_visualization_thread as thread



class Plot():
    """
    Class representing a plot with temperature information.

    Attributes:
        soc (socket.socket): Socket object for communication with the server.
        window (sg.Window): PySimpleGUI window object.
        my_thread (thread.ThreadClass): Custom thread object for updating the plot.
    """
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
        heat_fig_canvas = self.create_figure_resistance(self.window["-RES_PLOT-"].TKCanvas)
        fan_fig_canvas = self.create_figure_fan(self.window["-FAN_PLOT-"].TKCanvas)
        fig_canvas = (in_temp_fig_canvas, heat_fig_canvas, fan_fig_canvas)
        #initialize thread
        self.my_thread = thread.ThreadClass(self.window, fig_canvas)
        self.my_thread.start()


    
    def create_temps_figure(self, canvas) -> FigureCanvasTkAgg:
        """
            Creates and displays a temperature figure on a Tkinter canvas.

            Args:
                canvas: The Tkinter canvas object.

            Returns:
                FigureCanvasTkAgg: The created figure canvas.
        """
        fig:plt.Figure = plt.Figure(figsize=(10, 5), dpi=100, layout="constrained")
        plt.style.use("ggplot")
        t = np.arange(0, 3, .01)
        ax:axes.Axes = fig.add_subplot(111)
        ax.plot(t, 2 * np.sin(2 * np.pi * t), label='in_temp')
        ax.plot(t, 2 * np.sin(2 * np.pi * t)*4, label='out_temp')
        ax.axhline(y=0, color='r', linestyle='-')
        ax.axhline(y=0, color='r', linestyle='-')
        fig.supxlabel("time (s)")
        ax.legend()

        matplotlib.use("TkAgg")
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg
    
    def create_figure_resistance(self, canvas):
        """
            Creates and displays a figure for the resistance on a Tkinter canvas.

            Args:
                canvas: The Tkinter canvas object.

            Returns:
                FigureCanvasTkAgg: The created figure canvas.
        """
        fig:plt.Figure = plt.Figure(figsize=(5, 4), dpi=100, layout="constrained")
        plt.style.use("ggplot")
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot(111)
        ax.plot(t, 2 * np.sin(2 * np.pi * t))
        ax.set_ylim(0,100)
        ax.plot()
        fig.supxlabel("time (s)")

        matplotlib.use("TkAgg")
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg
    
    def create_figure_fan(self, canvas):
        """
            Creates and displays a figure for the fan on a Tkinter canvas.

            Args:
                canvas: The Tkinter canvas object.

            Returns:
                FigureCanvasTkAgg: The created figure canvas.
        """
        fig:plt.Figure = plt.Figure(figsize=(5, 4), dpi=100, layout="constrained")
        plt.style.use("ggplot")
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot(111)
        ax.set_xlabel("time (s)")
        ax.set_ylabel("% * (10)")
        ax.plot(t, 2 * np.sin(2 * np.pi * t))
        ax.plot()

        matplotlib.use("TkAgg")
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

    def update_state(self, temp:str, temp_int:str) -> None:
        """
            Updates the state display with temperature and interval information.

            Args:
                temp (str): Temperature value.
                temp_int (str): Temperature interval value.

            Returns:
                None
        """
        to_state = "Temp: " + str(temp) + "ºC and Interval: " + str(temp_int) + "ºC"
        self.window["-C_STATE-"].update(to_state)
        
    def update_file_path(self, file_path):
        self.file_path = file_path
        self.my_thread.update_data_filepath(file_path)  # Assuming you want to update the plot immediately after a new file is selected

        
    def kill_thread(self) -> None:
        """
            Stops the thread execution.

            Args:
                None

            Returns:
                None
        """
        self.my_thread.kill()

