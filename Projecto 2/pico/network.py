import network
import socket
import select
import time
import errno
import _thread
from sensor_data_acquisition import sensor_data_acquisition, initiate

DATA_RECORDER_PORT = 4443
CONFIGURATOR_PORT = 5554

ssid = "Quinta-dos-Sonhos"
password = "casadosazeites132"


mutex = _thread.allocate_lock()

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip

def open_socket(ip, port):
    address = (ip, port)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    connection.setblocking(False)  # Set the socket to non-blocking mode
    return connection

def receive_state(connection):
    state = 0
    print("here")
    while True:
        try:
            client, addr = connection.accept()
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
            break
        except OSError as e:
            if e.args[0] != errno.EAGAIN and e.args[0] != errno.EWOULDBLOCK:
                raise e
            else:
                break
    time.sleep_ms(1000)

def send_data(s, data):
    message = f"{time.time()};{data};0;0;0;0\n"
    s.sendall(bytes(message, 'ascii'))

def main():
    ip = connect()

    external_connection, internal_probe, roms = initiate(ip)

    connection = open_socket(ip, CONFIGURATOR_PORT)
    state = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.201', DATA_RECORDER_PORT))

    while True:
        
        sensor_data_acquisition(external_connection, internal_probe, roms)
        
        # Check for data from the CONFIGURATOR_PORT
        readable, _, _ = select.select([connection], [], [], 0)

        for sock in readable:
            if sock is connection:
                receive_state(connection)

        
        send_data(s, 23)
        time.sleep_ms(1000)

main()
