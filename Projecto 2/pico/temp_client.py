import network
import socket
import time
import machine
import onewire
import ds18x20

ssid = "Quinta-dos-Sonhos"
password = "casadosazeites132"

CLIENT_PORT = 5555
SERVER_PORT = 4444


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

def acquire_data():
    
    # Setup temperature probe
    ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(0)))
    roms = ds.scan()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to server")
    s.connect(('192.168.1.201',SERVER_PORT))
    
    while True:
      ds.convert_temp()
      time.sleep_ms(1000)
      for rom in roms:
        temp = ds.read_temp(rom)
        print(f"Current temperature: {temp}")
        send_data(s, temp)
      

def send_data(s, data):
    message = f"{time.time()};{data};0;0;0;0\n"
    s.sendall(bytes(message, 'ascii'))
    
def main():
    ip = connect()
    acquire_data()
    
main()
    
