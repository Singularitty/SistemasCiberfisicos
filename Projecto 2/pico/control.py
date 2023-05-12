import time
from actuation import Actuation

class PID:

    def __init__(self, Kp, Ki, Kd):
        
        # PID 
        self.Kp=Kp
        self.Ki=Ki
        self.Kd=Kd

        self.integral = 0
        self.last_value = 0
        self.last_error = 0
        self.last_update = time.time()
        
        self.max_integral = 10
        
    
    def compute(self, setpoint, value):
        now = time.time()
        dt = now - self.last_update

        # compute error
        error = setpoint - value

        # compute integral and derivative terms
        self.integral += error * dt
        if self.integral > self.max_integral:
            self.integral = self.max_integral
        
        derivative = (error - self.last_error) / dt

        # compute output
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # save state for next iteration
        self.last_error = error
        self.last_update = now

        return output

def in_activation_interval(internal, external, target, interval):
    if not (internal < target - interval or internal > target + interval):
        return False
    return True


def control(shared_temps, temps_lock, shared_target, target_lock, shared_actuations, actuations_lock):
    
    actuation = Actuation()
    
    # Adjust the PID values
    pid_controller = PID(34,0.1,18)
    
    target_temp = None
    target_interval = None

    current_temp_external = None
    current_temp_internal = None

    while True:
        
        temps_lock.acquire()
        if shared_temps[0] is not None:
            _, current_temp_internal, current_temp_external = shared_temps[0]
            shared_temps[0] = None
        temps_lock.release()
        
        target_lock.acquire()
        if shared_target[0] is not None:
            target_temp, target_interval = shared_target[0]
            shared_target[0] = None
        target_lock.release()
        
        
        if None not in (target_temp, target_interval, current_temp_external, current_temp_internal):
            
            target_temp = float(target_temp)
            target_interval = float(target_interval)
            current_temp_external = float(current_temp_external)
            current_temp_internal = float(current_temp_internal)
            
            if target_temp < current_temp_external:
                target_temp = current_temp_external
            
            if in_activation_interval(current_temp_internal, current_temp_external, target_temp, target_interval):
                output = pid_controller.compute(target_temp, current_temp_internal)
                output = max(min(output, 100), -10)
                print(output)
                if output < 0:
                    actuation.heating_off()
                    actuation.fan_set(abs(output))
                else:
                    actuation.fan_off()
                    actuation.heating_set(output)
            else:
                actuation.fan_off()
                actuation.heating_off()
        
        actuations_lock.acquire()
        shared_actuations[0] = actuation.get_state()
        actuations_lock.release()
        
        print(actuation.get_state())
        
        time.sleep_ms(2000)

