import network
import socket
import time
import machine
import onewire
import ds18x20
import select
import errno

# Define Pin where Internal Temperature sensor is connected
INTERNAL_SENSOR_PIN = machine.Pin(21, machine.Pin.OUT)
EXTERNAL_SENSOR_PIN = machine.Pin(18, machine.Pin.OUT)

def acquire_temperature(ds, roms):
    """
    Acquires temperature readings from a DS18X20 temperature sensor.

    Args:
        ds (ds18x20.DS18X20): DS18X20 instance for temperature sensing.
        roms (list): List of ROM addresses for connected DS18X20 sensors.

    Returns:
        float: Temperature reading in Celsius.
    """
    ds.convert_temp()
    for rom in roms:
        temp = ds.read_temp(rom)
        return temp

def initiate_sensors():
    """
    Initializes the internal and external temperature sensors.

    Returns:
        tuple: A tuple containing the internal_probe, roms_internal, external_probe, and roms_external.
               internal_probe: DS18X20 instance for internal temperature sensing.
               roms_internal: List of ROM addresses for internal temperature sensors.
               external_probe: DS18X20 instance for external temperature sensing.
               roms_external: List of ROM addresses for external temperature sensors.
    """
    # Setup Internal Temperature Probe
    internal_probe = ds18x20.DS18X20(onewire.OneWire(INTERNAL_SENSOR_PIN))
    roms_internal = internal_probe.scan()
    # Setup External Temperature Probe
    external_probe = ds18x20.DS18X20(onewire.OneWire(EXTERNAL_SENSOR_PIN))
    roms_external = external_probe.scan()
    
    return internal_probe, roms_internal, external_probe, roms_external

def sensor_data_acquisition(internal_probe, roms_internal, external_probe, roms_external, shared_mem, mutex):
    """
    Acquires temperature data from the internal and external temperature sensors.

    Args:
        internal_probe (ds18x20.DS18X20): DS18X20 instance for internal temperature sensing.
        roms_internal (list): List of ROM addresses for internal temperature sensors.
        external_probe (ds18x20.DS18X20): DS18X20 instance for external temperature sensing.
        roms_external (list): List of ROM addresses for external temperature sensors.
        shared_mem (list): List to store the acquired temperature data.
        mutex (_thread.lock): Mutex lock for shared memory access.

    Returns:
        tuple: A tuple containing the timestamp, internal temperature reading, and external temperature reading.
               If an exception occurs during data acquisition, it returns None.
    """
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
