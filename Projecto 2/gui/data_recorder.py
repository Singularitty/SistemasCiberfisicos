import socket
import sys
import os
import datetime
import signal
from time import sleep

HOST = ''
PORT = 4444


def interrupt_handler(signal, frame):
    """
    Signal handler function for interrupt signal (SIGINT).

    Args:
        signal: Signal number.
        frame: Current stack frame.

    Returns:
        None
    """
    print("Stopping data acquisition")
    sys.exit(0)


def data_acquisition(conn: socket, filename: str):
    """
    Function to handle data acquisition from the client and write it to a file.

    Args:
        conn (socket): Socket object for communication with the client.
        filename (str): Name of the file to store the data.

    Returns:
        None
    """
    buffer = ""

    while True:
        message = conn.recv(1024)
        if not message:
            print("Client disconnected")
            break

        message = str(message, 'ascii')
        buffer += message
        data = buffer.split("\n")
        buffer = data.pop()

        with open("./data/" + filename + ".csv", "a") as inp:
            for values in data:
                print(values)
                try:
                    print(values)
                    time, temp_in, temp_out, temp_target, temp_interval, fan, heat = values.split(";")
                    inp.write(f"{time},{temp_in},{temp_out},{temp_target},{temp_interval},{fan},{heat}\n")
                except Exception as err:
                    raise err
                    print(err)
                    sys.exit(1)
        sleep(2)


def main():
    """
    Main function to start the server and handle client connections.

    Args:
        None

    Returns:
        None
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.bind((HOST, PORT))
    except socket.error as message:
        print(message)
        sys.exit()

    print('Socket binding operation completed')

    soc.listen(9)

    if not os.path.exists("./data"):
        os.mkdir("./data")

    filename = datetime.datetime.now().strftime("%d:%m:%Y_%H:%M:%S")

    with open("./data/" + filename + ".csv", "w") as inp:
        inp.write(f"time,temp_in,temp_out,temp_target,temp_interval,fan,heat\n")

    print(f"Began data acquisition: {filename}")

    while True:
        conn, address = soc.accept()
        print('Connected with ' + address[0] + ':' + str(address[1]))

        try:
            data_acquisition(conn, filename)
        except socket.error as e:
            print(f"Socket error: {e}, waiting for a new connection...")
        finally:
            conn.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)
    main()