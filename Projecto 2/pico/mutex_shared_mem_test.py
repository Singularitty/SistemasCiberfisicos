import _thread
import time


global_arr = [0]

mutex = _thread.allocate_lock()

def t0(global_arr, mutex):
    while True:
        mutex.acquire()
        global_arr[0] = global_arr[0] + 1
        print("Thread0:", global_arr[0])
        mutex.release()
        time.sleep_ms(500)
    
def t1(global_arr, mutex):
    while True:
        mutex.acquire()
        global_arr[0] = global_arr[0] + 1
        print("Thread1:", global_arr[0])
        mutex.release()
        time.sleep_ms(500)
    
    
def main():
    _thread.start_new_thread(t1, ([global_arr, mutex]))
    t0(global_arr, mutex)
    
main()