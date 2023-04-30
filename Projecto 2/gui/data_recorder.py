import socket
import sys
import os
import datetime
import signal

HOST = ''
PORT = 4444


def interrupt_handler(signal, frame):
    print("Stopping data acquisition")
    sys.exit(0)

def data_acquisition(conn: socket):
    
    if not os.path.exists("./data"):
        os.mkdir("./data")
        
    buffer = ""
    
    filename = datetime.datetime.now().strftime("%d:%m:%Y_%H:%M:%S")
    
    print(f"Began data acquisition: {filename}")
    
    with open("./data/" + filename + ".csv", "w") as inp:
        inp.write(f"time,temp_in,temp_out,fan,heat,state\n")
        with conn:
            while True:
                message = str(conn.recv(1024), 'ascii')
                buffer += message
                data = buffer.split("\n")
                buffer = data.pop()  # store the last incomplete message for the next iteration

                for values in data:
                    print(values)
                    try:
                        time, temp_in, temp_out, fan, heat, state = values.split(";")
                        inp.write(f"{time},{temp_in},{temp_out},{fan},{heat},{state}\n")
                    except Exception as err:
                        print(err)
                        sys.exit(1)
            

def main():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.bind((HOST, PORT))

    except socket.error as message:
        print('Bind failed. Error Code : '
              + str(message[0]) + ' Message '
              + message[1])
        sys.exit()


    # print if Socket binding operation completed   
    print('Socket binding operation completed')
    
    # With the help of listening () function
    # starts listening
    soc.listen(9)
    
    conn, address = soc.accept()
    # print the address of connection
    print('Connected with ' + address[0] + ':'
          + str(address[1]))
    
    data_acquisition(conn)
    
      
if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)
    main()
