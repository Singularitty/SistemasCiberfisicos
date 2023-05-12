import network
import socket
import time
import machine
import onewire
import ds18x20
import select
import errno

# Define Pin where Internal Temperature sensor is connected
INTERNAL_SENSOR_PIN = machine.Pin(20, machine.Pin.OUT)
EXTERNAL_SENSOR_PIN = machine.Pin(18, machine.Pin.OUT)

def acquire_temperature(ds, roms):
    ds.convert_temp()
    for rom in roms:
        temp = ds.read_temp(rom)
        return temp

def initiate_sensors():
    # Setup Internal Temperature Probe
    internal_probe = ds18x20.DS18X20(onewire.OneWire(INTERNAL_SENSOR_PIN))
    roms_internal = internal_probe.scan()
    # Setup External Temperature Probe
    external_probe = ds18x20.DS18X20(onewire.OneWire(EXTERNAL_SENSOR_PIN))
    roms_external = external_probe.scan()
    
    return internal_probe, roms_internal, external_probe, roms_external

def sensor_data_acquisition(internal_probe, roms_internal, external_probe, roms_external, shared_mem, mutex):
    try:
        internal_reading = acquire_temperature(internal_probe, roms_internal)
        external_reading = acquire_temperature(external_probe, roms_external)
        timestamp = time.time()
        mutex.acquire()
        shared_mem[0] = (timestamp, internal_reading, external_reading)
        mutex.release()
        return timestamp, internal_reading, external_reading
    except:
        print("Re-initializing Temperature Probes")
        time.sleep_ms(100)
        internal_probe, roms_internal, external_probe, roms_external = initiate_sensors()
        return None
