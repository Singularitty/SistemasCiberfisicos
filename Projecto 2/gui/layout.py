import PySimpleGUI as sg

def create_window() -> sg.Window:
    state = [
        [
            sg.Text("Current State"),
            sg.Text(size=(40, 1), key="-C_STATE-")
        ],
        [
            sg.Text("Choose temperature:"),
            sg.In(size=(5, 1), enable_events=True, key="-IN_TEMP_VALUE-")
        ],
        [
            sg.Text("Choose interval:"),
            sg.In(size=(5, 1), enable_events=True, key="-TEMP_INT-")
        ],
        [
            sg.Button("Send Values")
        ]
    ]

    temperature_layout = [
        [sg.Text("Temperature plot")],
        [sg.Canvas(key="-TEMP_PLOT-")]
    ]

    resistance_layout = [
        [sg.Text("Resistance plot")],
        [sg.Canvas(key="-RES_PLOT-")]
    ]

    fan_layout = [
        [sg.Text("Fan plot")],
        [sg.Canvas(key="-FAN_PLOT-")]
    ]

    full_layout = [
        [
            sg.Column(state),
            sg.Column(temperature_layout),
        ],[
            sg.Column(resistance_layout),
            sg.Column(fan_layout),
        ]
    ]

    # Create the form and show it without the plot
    window = sg.Window(
        "Data Visualization Component",
        full_layout,
        location=(0, 0),
        finalize=True,
        element_justification="right",
        font="Helvetica 18",
        size=(1280,800)
    )

    return window