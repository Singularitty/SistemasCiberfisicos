import network
import socket
import time
import machine

PI_SERVER_PORT = 5555

def open_socket(ip):
    address = (ip, PI_SERVER_PORT)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def server(connection):
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
    connection = open_socket(ip)
    server(connection)