from machine import Pin, PWM

class Actuation:
    
    def __init__(self, heating_pin = 16, heating_freq = 1000, fan_pin = 15, fan_freq = 10000):
        # Define PWM output for PIN Corresponding to the heating element
        self.heating = PWM(Pin(heating_ping, Pin.OUT))
        self.heating.freq(heating_freq)

        # Define PWM output for PIN Corresponding to the fan
        self.fan = PWM(Pin(fan_pin, Pin.OUT))
        self.fan.freq(fan_freq)
        
        self.fan_state = 0
        self.heat_state = 0


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
    
    def heating_set(self, target):
        """
        Set the heating element to the specified target (unsigned 16 bit int)
        """
        self.heating.duty_u16(target)
        self.heat_state = target
    
    def fan_set(self, target):
        """
        Set the heating element to the specified target (unsigned 16 bit int)
        """
        self.fan.duty_u16(target)
        self.fan_state = target
        
    def get_state(self):
        """
        Return current actuation states
        """
        return self.fan_state, self.heat_state
        