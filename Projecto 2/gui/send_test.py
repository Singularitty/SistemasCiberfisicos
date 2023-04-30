import socket
import random
import time

HOST = ""  # The server's hostname or IP address
PORT = 4444  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        time.sleep(0.1)
        tempo = time.time()
        temp_in = random.randint(-100,100) + random.random()
        temp_out = random.randint(-100,100) + random.random()
        state = random.randint(0, 5)
        fan = random.random() * 100
        heat = random.random() * 50
        message = f"{tempo};{temp_in};{temp_out};{fan};{heat};{state}\n"
        s.sendall(bytes(message, 'ascii'))