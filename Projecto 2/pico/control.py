import time

class PID:

    def __init__(self, Kp, Ki, Kd, shared_mem_temps, temperatures_lock, shared_mem_targets, targets_lock):
        
        self.Kp=Kp
        self.Ki=Ki
        self.Kd=Kd
        
        self.shared_mem_targets = shared_mem_targets
        self.targets_lock = targets_lock

        self.shared_mem_temps = shared_mem_temps
        self.temperatures_lock = temperatures_lock

        self.integral = 0
        self.last_value = 0
        self.last_error = 0
        self.lastupdate = None

    def control(self):
        pass
    
    