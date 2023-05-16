import socket

HOST = "192.168.100.131" #"192.168.30.219"  # The server's hostname or IP address
PORT = 5555  # The port used by the server

def create_socket(HOST:str, PORT:int) -> socket:
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

def configurator(targets:str) -> None:
    """
        Sends temperature information to the server.
        Args:
            targets (str): Temperature information to send.
        Returns:
            None
    """
    soc = create_socket(HOST, PORT) #TODO
    message = bytes(targets, "ascii")
    soc.sendall(message)
    soc.close()
