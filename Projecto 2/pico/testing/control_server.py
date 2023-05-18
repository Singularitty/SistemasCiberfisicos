import network
import socket
import time
import machine

PI_SERVER_PORT = 5555

def open_socket(ip):
    """
    Open a socket connection for communication.

    Args:
        ip (str): IP address of the server.

    Returns:
        connection (socket.socket): Socket connection object.

    Raises:
        OSError: If the socket cannot be opened or bound.
    """
    address = (ip, PI_SERVER_PORT)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def server(connection):
    """
    Start the server to receive messages from clients.

    Args:
        connection (socket.socket): Socket connection object.

    Returns:
        None
    """
    state = 0
    while True:
        print("hello")
        client = connection.accept()[0]
        message = client.recv(1024)
        message = str(message)
        try:
            new_state = message.split("\\n")[0]
        except IndexError:
            pass
        if new_state == state:
            print("No change in state")
        else:
            print(f"Changed state to {new_state}")
        client.close()
        time.sleep_ms(1000)
        
def thread1(ip):
    """
    Thread 1 function to open a socket connection and start the server.

    Args:
        ip (str): IP address of the server.

    Returns:
        None
    """
    connection = open_socket(ip)
    server(connection)