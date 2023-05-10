import network
import socket
import select
import time
import errno
import _thread
from sensor_data_acquisition import sensor_data_acquisition, initiate_sensors
# from control import *

# Network Configuration
DATA_RECORDER_PORT = 4444
DATA_RECORDER_IP = ''
CONFIGURATOR_PORT = 5555

SSID = ""
PASSWORD = ""


# Global memory for temperatures
shared_mem_temperatures = []
temperatures_lock = _thread.allocate_lock()

# Global memory for control targets
shared_mem_targets = []
targets_lock = _thread.allocate_lock()


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSDI, PASSWORD)
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
    target_temp = None
    target_error = None
    while True:
        try:
            client, _ = connection.accept()
            message = client.recv(1024)
            message = message.decode("utf-8")
            try:
                data = message.split("\\n")[0]
                target_temp, target_error = data.split(";")
            except IndexError:
                pass
            client.close()
            return target_temp, target_error
        except OSError as e:
            if e.args[0] != errno.EAGAIN and e.args[0] != errno.EWOULDBLOCK:
                raise e
            else:
                break

def send_data(s, timestamp, internal_temp, external_temp, temp_target, temp_target_error, fan_target, heat_target):
    message = f"{timestamp};{internal_temp};{external_temp};{temp_target};{temp_target_error};{fan_target};{heat_target}\n"
    s.sendall(bytes(message, 'ascii'))

def main():

    ip = connect()

    # Open socket for configurator to talk pico
    connection = open_socket(ip, CONFIGURATOR_PORT)

    # Connect to data recorder
    data_recorder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_recorder_socket.connect((DATA_RECORDER_IP, DATA_RECORDER_PORT))
    
    # Initiate Temperature Sensors
    initiate_sensors()
    
    # Launch Control Thread
    # TODO

    while True:
        
        # Acquire temperatures
        timestamp, intertal_temp, external_temp = sensor_data_acquisition()
        
        
        target_temp = None
        target_error = None
        # Check for data from the CONFIGURATOR_PORT
        readable, _, _ = select.select([connection], [], [], 0)
        # If there is data, read from socket
        for sock in readable:
            if sock is connection:
                target_temp, target_error = receive_targets(connection)

        # write new targets memory shared with control
        # TODO
        
        # Send data to data recorder
        send_data(data_recorder_socket,
                  timestamp,
                  intertal_temp,
                  external_temp,
                  target_temp,
                  target_error,
                  0,
                  0)
        
        time.sleep_ms(1000)

main()
