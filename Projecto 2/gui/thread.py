import threading
import PySimpleGUI as sg
import os
from datetime import datetime
import pandas as pd

DATETIME_FORMAT = "%d:%m:%Y_%H:%M:%S"

class ThreadClass(threading.Thread):
    window:sg.Window
    is_killed:bool

    def __init__(self, window:sg.Window) -> None:
        threading.Thread.__init__(self)
        self.window = window
        self.is_killed = False

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
        # create dataframe
        dataframe = pd.read_csv(filepath)
        while not self.is_killed:
            # receive info from socket and update plot
            pass

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
            if closest_datetime < date[0]:
                closest_datetime = date
        return closest_datetime

    def kill(self) -> None:
        self.is_killed = True

