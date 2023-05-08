from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import PySimpleGUI as sg
from datetime import datetime
import pandas as pd
import os
from time import sleep

DATETIME_FORMAT = "%d:%m:%Y_%H:%M:%S"

class ThreadClass(threading.Thread):
    window:sg.Window
    is_killed:bool
    axes:tuple

    def __init__(self, window:sg.Window, fig_canvas:tuple) -> None:
        threading.Thread.__init__(self)
        self.window = window
        self.is_killed = False
        self.fig_canvas = fig_canvas

    def run(self) -> None:
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
        
        (temp_fig_canva, heat_fig_canva, fan_fig_canva) = self.fig_canvas
        
        while not self.is_killed:
            # create dataframe
            dataframe:pd.DataFrame = pd.read_csv(filepath) 
            temp_fig_canva = self.update_figure(dataframe, "temp_in", temp_fig_canva)
            heat_fig_canva = self.update_figure(self.window["-RES_PLOT-"].TKCanvas, dataframe, "fan", heat_fig_canva)
            fan_fig_canva = self.update_figure(self.window["-FAN_PLOT-"].TKCanvas, dataframe, "heat", fan_fig_canva)
            sleep(2)

    def str_list_to_datetime_list(self, filenames_list:list[str]) -> list[datetime]:
        datetime_list:list[datetime] = []
        for filename in filenames_list:
            filename = filename.replace(".csv", "")
            date_time = datetime.strptime(filename, DATETIME_FORMAT)
            datetime_list.append(date_time)
        return datetime_list
    
    def closest_datetime(self, datetime_list:list[datetime]) -> datetime:
        if len(datetime_list) == 1:
            return datetime_list[0]
        closest_datetime:datetime = datetime_list[0]
        for date in datetime_list:
            if closest_datetime < date:
                closest_datetime = date
        return closest_datetime

    def kill(self) -> None:
        self.is_killed = True

    def update_temps_figure(self, dataframe:pd.DataFrame, in_temp_string:str, out_temp_string:str, fig_canva:FigureCanvasTkAgg):
        """
            Updates the figure Canvas of temperatures 
        """
        fig:plt.Figure = plt.Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(dataframe.loc[:, "time"], dataframe.loc[:, in_temp_string], dataframe[:, "time"], dataframe.loc[:, out_temp_string])
        fig_canva.figure = fig
        fig_canva.draw()
        fig_canva.get_tk_widget().pack(side="top", fill="both", expand=1)
        return fig_canva


    def update_figure(self, canvas, dataframe:pd.DataFrame, y_value:str, fig_canva:FigureCanvasTkAgg):
        fig:plt.Figure = plt.Figure(figsize=(3, 3), dpi=100)
        fig.add_subplot(111).plot(dataframe.loc[:, "time"], dataframe.loc[:, y_value])
        fig_canva.figure = fig
        fig_canva.draw()
        fig_canva.get_tk_widget().pack(side="top", fill="both", expand=1)
        return fig_canva

