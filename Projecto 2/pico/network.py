import network
import socket
import select
import time
import errno
import _thread
from sensor_data_acquisition import sensor_data_acquisition, initiate_sensors
# from control import *

DATA_RECORDER_PORT = 4444
DATA_RECORDER_IP = ''
CONFIGURATOR_PORT = 5555

ssid = ""
password = ""


# Global memory for temperatures
shared_mem_temperatures = []
temperatures_lock = _thread.allocate_lock()

# Global memory for control targets
shared_mem_targets = []
targets_lock = _thread.allocate_lock()


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

def receive_targets(connection):
    state = 0
    print("here")
    while True:
        try:
            client, _ = connection.accept()
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

def send_data(s, timestamp, internal_temp, external_temp, temp_target, temp_target_error, fan_target, heat_target):
    message = f"{timestamp};{internal_temp};{external_temp};{temp_target};{temp_target_error};{fan_target};{heat_target}\n"
    s.sendall(bytes(message, 'ascii'))

def main():

    ip = connect()

    # Open socket for configurator to talk pico
    connection = open_socket(ip, CONFIGURATOR_PORT)

    # Connect to data recorder
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((DATA_RECORDER_IP, DATA_RECORDER_PORT))
    
    # Initiate Temperature Sensors
    initiate_sensors()
    
    # Launch Control Thread
    # TODO

    while True:
        
        # Acquire temperatures
        timestamp, intertal_temp, external_temp = sensor_data_acquisition()
        
        # Check for data from the CONFIGURATOR_PORT
        readable, _, _ = select.select([connection], [], [], 0)
        # If there is data, read from socket
        for sock in readable:
            if sock is connection:
                receive_targets(connection)

        # write new targets memory shared with control
        # TODO
        
        # Send data to data recorder
        send_data(s, 23)
        
        time.sleep_ms(1000)

main()
