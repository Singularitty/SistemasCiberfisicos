import network
import socket
import select
import time
import errno
import _thread
from sensor_data_acquisition import sensor_data_acquisition, initiate_sensors
from control import control

# Network Configuration
DATA_RECORDER_PORT = 4444
DATA_RECORDER_IP = '192.168.30.169'
CONFIGURATOR_PORT = 5555
SSID = "pico1"
PASSWORD = "random123"

# Global memory for temperatures
shared_mem_temperatures = [None]
temperatures_lock = _thread.allocate_lock()

# Global memory for control targets
shared_mem_targets = [None]
targets_lock = _thread.allocate_lock()

# Global memory for actuations states
shared_actuation_state = [None]
actuation_lock = _thread.allocate_lock()


def connect():
    """
    Connects to a Wi-Fi network using the provided SSID and PASSWORD.

    Returns:
        str: The IP address assigned to the device.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip

def open_socket(ip, port):
    """
    Opens a socket and binds it to the specified IP address and port.

    Args:
        ip (str): IP address to bind the socket.
        port (int): Port number to bind the socket.

    Returns:
        socket.socket: The created and bound socket.
    """
    address = (ip, port)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    connection.setblocking(True)  # Set the socket to blocking mode
    return connection

def receive_targets(connection):
    """
    Receives target temperature and error values from the configurator.

    Args:
        connection (socket.socket): The socket connection with the configurator.

    Returns:
        tuple: The received target temperature and error values.
    """
    target_temp = None
    target_error = None
    while True:
        try:
            client, _ = connection.accept()
            message = client.recv(1024)
            message = message.decode("utf-8")
            print(message)
            try:
                data = message.split("\\n")[0]
                target_temp, target_error = data.strip().split(";")
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
    """
    Sends the data to the data recorder.

    Args:
        s (socket.socket): The socket connection with the data recorder.
        timestamp (int): Timestamp of the data.
        internal_temp (float): Internal temperature value.
        external_temp (float): External temperature value.
        temp_target (float): Target temperature value.
        temp_target_error (float): Target temperature error value.
        fan_target (int): Fan target value.
        heat_target (int): Heating target value.

    Returns:
        None
    """
    message = f"{timestamp};{internal_temp};{external_temp};{temp_target};{temp_target_error};{fan_target};{heat_target}\n"
    s.sendall(bytes(message, 'ascii'))

def main():
    """
    Main function that orchestrates the data recording, temperature sensing, and control processes.

    Returns:
        None
    """

    ip = connect()

    # Open socket for configurator to talk pico
    connection = open_socket(ip, CONFIGURATOR_PORT)

    # Connect to data recorder
    data_recorder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_recorder_socket.connect((DATA_RECORDER_IP, DATA_RECORDER_PORT))
    
    # Initiate Temperature Sensors
    internal_probe, roms_internal, external_probe, roms_external = initiate_sensors()
    
    # Launch Control Thread
    _thread.start_new_thread(control, [shared_mem_temperatures, temperatures_lock,
                                       shared_mem_targets, targets_lock,
                                       shared_actuation_state, actuation_lock])
    
    target_temp = None
    target_error = None
    
    fan_target = 0
    heat_target = 0

    while True:
        
        # Acquire temperatures
        acquisition = sensor_data_acquisition(internal_probe,
                                              roms_internal,
                                              external_probe,
                                              roms_external,
                                              shared_mem_temperatures,
                                              temperatures_lock)
        
        # Inside temperature probe sometimes returns nothing
        # Causing the sensor_data_acquisition to reinitiate the probes
        # In that case we skip that iteration
        if acquisition is not None:
            timestamp, intertal_temp, external_temp = acquisition

            # Check for data from the CONFIGURATOR_PORT
            readable, _, _ = select.select([connection], [], [], 0)
            # If there is data, read from socket
            for sock in readable:
                if sock is connection:
                    temp, interval = receive_targets(connection)
                    if temp is not None and interval is not None:
                        target_temp = temp
                        target_error = interval

            # write new targets in memory shared with control thread
            if target_temp is not None and target_error is not None:
                targets_lock.acquire()
                shared_mem_targets[0] = (target_temp, target_error)
                targets_lock.release()
        
            # Get current actuation states from shared memory
            actuation_lock.acquire()
            if shared_actuation_state[0] is not None:
                fan_target, heat_target = shared_actuation_state[0]
                shared_actuation_state[0] = None
            actuation_lock.release()
        
        
            # Send data to data recorder
            send_data(data_recorder_socket,
                      timestamp,
                      intertal_temp,
                      external_temp,
                      target_temp,
                      target_error,
                      fan_target,
                      heat_target)
        
        time.sleep_ms(1000)

main()
