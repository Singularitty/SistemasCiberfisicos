from machine import Pin, PWM
import time

class Actuation:
    
    def __init__(self, heating_pin = 16, heating_freq = 1000, fan_pin = 15, fan_freq = 100000):
        # Define PWM output for PIN Corresponding to the heating element
        self.heating = PWM(Pin(heating_pin, Pin.OUT))
        self.heating.freq(heating_freq)

        # Define PWM output for PIN Corresponding to the fan
        self.fan = PWM(Pin(fan_pin, Pin.OUT))
        self.fan.freq(fan_freq)
        
        self.heating_max = heating_freq
        self.fan_max = fan_freq
        
        # Actuation state in percentage
        self.fan_state = 0
        self.heat_state = 0
        
        # Actual Duty value
        self._fan_duty = 0
        self._heat_duty = 0

        # Make sure components are off when initializing actuation component
        self.fan_off()
        self.heating_off()


    def heating_off(self):
        """
        Turn of the heating element
        """
        self.heating.duty_u16(0)
        self.heat_state = 0
    
    def fan_off(self):
        """
        Turn off the fan
        """
        self.fan.duty_u16(0)
        self.fan_state = 0
    
    def heating_set(self, percentage):
        """
        Set the heating element to the specified target (0-100%)
        """
        target = percentage * 10
        self.heating.duty_u16(target)
        self.heat_state = percentage
        self._heat_duty = target
    
    def fan_set(self, percentage):
        """
        Set the heating element to the specified target (unsigned 16 bit int)
        """
        target = 57500 + percentage * 25 # range de 57500-60000
        self.fan.duty_u16(target)
        self.fan_state = percentage
        self._fan_duty = target
        
    def get_state(self):
        """
        Return current actuation states
        """
        return self.fan_state, self.heat_state

        
    def __fan_cycle(self):
        # For testing
        c = 0
        for i in range(100):
            c += 1000000 // 100
            print(c)
            self.fan_set(c)
            time.sleep(0.1)
            
    def __get_duty(self):
        # For debugging
        return self._fan_duty, self._heat_duty