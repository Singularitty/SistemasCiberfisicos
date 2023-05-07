import socket
import random
import time

HOST = "192.168.1.210"  # The server's hostname or IP address
PORT = 3333 # The port used by the server

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

while True:
    with connect_to_server() as s:
        try:
            print("connected")
            time.sleep(0.1)
            tempo = time.time()
            temp_in = random.randint(-100, 100) + random.random()
            temp_out = random.randint(-100, 100) + random.random()
            state = random.randint(0, 5)
            fan = random.random() * 100
            heat = random.random() * 50
            message = f"{time.time()};{temp_out}\n"
            print("sending data")
            s.sendall(bytes(message, 'ascii'))
            time.sleep(1)
        except socket.error as e:
            print(f"Socket error: {e}, reconnecting...")
            time.sleep(1)
