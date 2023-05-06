import network
import socket
import time
import machine
import onewire
import ds18x20
import select
import errno


# Pico will listen to this port to recieve external temp readings
EXTERNAL_TEMP_PORT = 3333

# Define Pin where Internal Temperature sensor is connected
INTERNAL_SENSOR_PIN = machine.Pin(14, machine.Pin.OUT)


def open_socket(ip, port):
    address = (ip, port)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    return connection


def acquire_external_temperature(connection):
    while True:
        try:
            client, _ = connection.accept()
            message = client.recv(1024)
            message = str(message)
            try:
                timestamp, external_temp  = message.split("\\n")[-1].split(";")
            except IndexError:
                pass
            client.close()
            return timestamp, external_temp
        except OSError as e:
            if e.args[0] != errno.EAGAIN and e.args[0] != errno.EWOULDBLOCK:
                raise e
            else:
                break

def acquire_interal_temperature(ds, roms):
    ds.convert_temp()
    for rom in roms:
        temp = ds.read_temp(rom)
        return time.time(), temp

def sensor_data_acquisition(ip, shared_mem, mutex):

    # Setup Internal Temperature Probe
    internal_probe = ds18x20.DS18X20(onewire.OneWire(INTERNAL_SENSOR_PIN))
    roms = internal_probe.scan()
    
    # Open socket to receive external temperature readings
    connection = open_socket(ip, EXTERNAL_TEMP_PORT)
    
    while True:
        # Check for data from the EXTERN_TEMP_PORT
        readable, _, _  = select.select([connection], [], [], 0)
        
        # Attempt to Acquire External Temperature Reading
        current_external_reading = None
        for sock in readable:
            if sock is connection:
                current_external_reading = acquire_external_temperature(connection)
        
        # Acquire Internal Temperature Reading
        current_internal_reading = acquire_interal_temperature(internal_probe, roms)
        
        print(current_external_reading)
        print(current_internal_reading)
        
        time.sleep_ms(1000)