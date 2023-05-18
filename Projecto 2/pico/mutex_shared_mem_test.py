import _thread
import time


global_arr = [0]

mutex = _thread.allocate_lock()

def t0(global_arr, mutex):
    """
    Thread function that increments the value in global_arr by 1 and prints it.
    
    Args:
        global_arr (list): Shared list containing a single value.
        mutex (_thread.LockType): Mutex lock for synchronizing access to global_arr.
    
    Returns:
        None
    """
    while True:
        mutex.acquire()
        global_arr[0] = global_arr[0] + 1
        print("Thread0:", global_arr[0])
        mutex.release()
        time.sleep_ms(500)
    
def t1(global_arr, mutex):
    """
    Thread function that increments the value in global_arr by 1 and prints it.
    
    Args:
        global_arr (list): Shared list containing a single value.
        mutex (_thread.LockType): Mutex lock for synchronizing access to global_arr.
    
    Returns:
        None
    """
    while True:
        mutex.acquire()
        global_arr[0] = global_arr[0] + 1
        print("Thread1:", global_arr[0])
        mutex.release()
        time.sleep_ms(500)
    
    
def main():
    """
    Main function that starts two threads: t1 and t0.
    
    Returns:
        None
    """
    _thread.start_new_thread(t1, ([global_arr, mutex]))
    t0(global_arr, mutex)
    
main()