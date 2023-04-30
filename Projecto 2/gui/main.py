from plot import Plot
import PySimpleGUI as sg

def main():
    my_plot = Plot()

    # Add the plot to the window
    my_plot.update_figure(my_plot.window["-INT_TEMP_PLOT-"].TKCanvas)
    my_plot.update_figure(my_plot.window["-OUT_TEMP_PLOT-"].TKCanvas)
    my_plot.update_figure(my_plot.window["-RES_PLOT-"].TKCanvas)
    my_plot.update_figure(my_plot.window["-FAN_PLOT-"].TKCanvas)

    while True:
        event, values = my_plot.window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Send Values":
            temp = values["-IN_TEMP_VALUE-"]
            temp_int = values["-TEMP_INT-"]
            to_deliver = temp + ";" + temp_int
            
            #my_plot.send_temp_info(to_deliver)

            my_plot.update_state(temp, temp_int)
            
            

            # send values throught socket
            pass
            

    my_plot.window.close()

    my_plot.kill_thread()

if __name__== "__main__" :
    main()