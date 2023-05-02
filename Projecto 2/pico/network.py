import network
import socket
import select
import time

DATA_RECORDER_PORT = 4443
CONFIGURATOR_PORT = 5554

ssid = ""
password = ""

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
    print("HEHRHE")
    try:
        client, addr = connection.accept()
        try:
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
        except OSError as e:
            if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
                print("No data received")
            else:
                raise e
        finally:
            client.close()
    except OSError as e:
        raise e
    time.sleep_ms(1000)



def send_data(s, data):
    message = f"{time.time()};{data};0;0;0;0\n"
    s.sendall(bytes(message, 'ascii'))

def main():
    ip = connect()
    connection = open_socket(ip, CONFIGURATOR_PORT)
    state = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.201', DATA_RECORDER_PORT))
    
    while True:
        for i in range(10):
            send_data(s, 23)
            time.sleep_ms(500)
        receive_state(connection)
    

main()
