import os
import threading
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Lock, Thread
from datetime import datetime
from matplotlib import axes
from time import sleep


DATETIME_FORMAT = "%d:%m:%Y_%H:%M:%S"

class ThreadClass(threading.Thread):
    """
        A class to create and manage the thread for updating the GUI.

        Attributes:
        window (sg.Window): The PySimpleGUI window object.
        is_killed (bool): A flag to indicate if the thread is stopped.
        fig_canvas (tuple): A tuple containing the FigureCanvasTkAgg objects for the 3 plots.
    """
    window:sg.Window
    is_killed:bool
    fig_canvas:tuple

    def __init__(self, window:sg.Window, fig_canvas:tuple) -> None:
        """
            Initializes the ThreadClass object.

            Args:
            window (sg.Window): The PySimpleGUI window object.
            fig_canvas (tuple): A tuple containing the FigureCanvasTkAgg objects for the 3 plots.
        """
        Thread.__init__(self)
        self.window = window
        self.is_killed = False
        self.fig_canvas = fig_canvas
        
        self.data_filepath = self.__determine_most_recent_file()
        
    def __determine_most_recent_file(self) -> str:
        # get filenames from ./data/ folder
        filenames_list:list[str] = os.listdir('./data/') 
        # convert list[str] to list[datetime]
        datetimes_list:list[datetime] = self.str_list_to_datetime_list(filenames_list) 
        # get the closest datetime
        closest_datetime:datetime = self.closest_datetime(datetimes_list)
        # convert closest datetime to str
        filename:str = closest_datetime.strftime(DATETIME_FORMAT)
        # apply filename path
        filepath:str = "./data/" + filename + ".csv"
        
        return filepath
    
    def update_data_filepath(self, filepath: str) -> None:
        """
            Updates the data filepath

            Args:
            filepath (str): The filepath string
        """
        self.data_filepath = filepath

    def run(self) -> None:
        """
            Continuously reads data from CSV files and updates the plots in real-time.
        """
        
        (temp_fig_canva, heat_fig_canva, fan_fig_canva) = self.fig_canvas
        
        while not self.is_killed:
            # create dataframe and update plots
            dataframe:pd.DataFrame = pd.read_csv(self.data_filepath) 
            temp_fig_canva = self.update_temps_figure(dataframe, temp_fig_canva)
            heat_fig_canva = self.update_figure(dataframe, "heat", heat_fig_canva, 100)
            fan_fig_canva = self.update_figure(dataframe, "fan", fan_fig_canva, 10)
            sleep(2)

    def str_list_to_datetime_list(self, filenames_list:list[str]) -> list[datetime]:
        """
            Converts a list of filenames to a list of corresponding datetimes.

            Parameters:
            -----------
            filenames_list : list[str]
                The list of filenames to convert.

            Returns:
            --------
            list[datetime]
                The list of corresponding datetimes.
        """
        datetime_list:list[datetime] = []
        for filename in filenames_list:
            filename = filename.replace(".csv", "")
            date_time = datetime.strptime(filename, DATETIME_FORMAT)
            datetime_list.append(date_time)
        return datetime_list
    
    def closest_datetime(self, datetime_list:list[datetime]) -> datetime:
        """
            Finds the closest datetime from a list of datetimes.

            Parameters:
            -----------
            datetime_list : list[datetime]
                The list of datetimes.

            Returns:
            --------
            datetime
                The closest datetime.
        """
        if len(datetime_list) == 1:
            return datetime_list[0]
        closest_datetime:datetime = datetime_list[0]
        for date in datetime_list:
            if closest_datetime < date:
                closest_datetime = date
        return closest_datetime

    def kill(self) -> None:
        """
            Stops the execution of the ThreadClass by setting the `is_killed` flag to True.
        """
        self.is_killed = True

    def update_temps_figure(self, dataframe:pd.DataFrame, fig_canva:FigureCanvasTkAgg) -> FigureCanvasTkAgg:
        """
            Updates the temperature plot with the latest data from the dataframe.

            Args:
            dataframe (pd.DataFrame): The dataframe containing the temperature data.
            fig_canva (FigureCanvasTkAgg): The FigureCanvasTkAgg object for the temperature plot.

            Returns:
            FigureCanvasTkAgg: The updated FigureCanvasTkAgg object.
        """
        fig:plt.Figure = plt.Figure(figsize=(10, 5), dpi=100, layout="constrained")
        ax:axes.Axes = fig.add_subplot(111)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (ºC)")
        ax.plot(dataframe.loc[:, "time"], dataframe.loc[:, "temp_in"], label='Interior Temperature')
        ax.plot(dataframe.loc[:, "time"], dataframe.loc[:, "temp_out"], label='Exterior Temperature')
        dataframe["temp_target"].map(lambda x: np.nan if x is None else x)
        dataframe["temp_interval"].map(lambda x: np.nan if x is None or x == 0 else x)
        dataframe["upper_bound"] = dataframe["temp_target"] + dataframe["temp_interval"]
        dataframe["lower_bound"] = dataframe["temp_target"] - dataframe["temp_interval"]
        ax.plot(dataframe.loc[:, "time"], dataframe.loc[:, "upper_bound"], label='Interval', color="gray")
        ax.plot(dataframe.loc[:, "time"], dataframe.loc[:, "lower_bound"], color="gray")
        ax.plot(dataframe.loc[:, "time"], dataframe.loc[:, "temp_target"], label='Target Temperature', color="black")
        #    upper_bound:float = temp_target + temp_interval
        #    lower_bound:float = temp_target - temp_interval
        #    ax.axhline(y=upper_bound, color='r', linestyle='-')
        #    ax.axhline(y=lower_bound, color='r', linestyle='-')
        ax.legend()
        fig_canva.figure = fig
        fig_canva.draw()
        fig_canva.get_tk_widget().pack(side="top", fill="both", expand=1)
        return fig_canva

    def update_figure(self, dataframe:pd.DataFrame, y_value:str, fig_canva:FigureCanvasTkAgg, ylimit: int) -> FigureCanvasTkAgg:
        """
            Updates a specific plot (fan or heat) with the latest data from the dataframe.

            Args:
            dataframe (pd.DataFrame): The dataframe containing the data for the plot.
            y_value (str): The name of the column in the dataframe to be plotted.
            fig_canva (FigureCanvasTkAgg): The FigureCanvasTkAgg object for the plot.

            Returns:
            FigureCanvasTkAgg: The updated FigureCanvasTkAgg object.
        """
        fig:plt.Figure = plt.Figure(figsize=(5, 4), dpi=100, layout="constrained")
        ax = fig.add_subplot(111)
        if y_value == "heat":
            ax.set_ylabel("Actuation %")
        else:
            ax.set_ylabel("Actuation % * (10)")
        ax.set_xlabel("Time (s)")
        ax.set_ylim(0, ylimit+1)
        ax.plot(dataframe.loc[:, "time"], dataframe.loc[:, y_value])
        fig_canva.figure = fig
        fig_canva.draw()
        fig_canva.get_tk_widget().pack(side="top", fill="both", expand=1)
        return fig_canva

