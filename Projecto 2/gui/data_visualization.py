import PySimpleGUI as sg
from data_visualization_plot import Plot
from configurator import configurator

def data_visualization():
    """
    Function to run the data visualization component.

    Args:
        None

    Returns:
        None
    """
    my_plot = Plot()
    while True:
        event, values = my_plot.window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Send Values":
            temp = values["-IN_TEMP_VALUE-"]
            temp_int = values["-TEMP_INT-"]
            try:
                temp = float(temp)
                temp_int = float(temp_int)
                to_deliver = f"{temp};{temp_int}\n"
                configurator(to_deliver)
                my_plot.update_state(temp, temp_int)
            except Exception as e:
                sg.popup('Please input numeric values')
        elif event == 'View data':
            file_path = values[0]  # The file path is in the first element of the values dictionary
            my_plot.update_file_path(file_path)


    my_plot.window.close()

    my_plot.kill_thread()

if __name__== "__main__" :
    data_visualization()
