from machine import Pin, PWM
from time import sleep

pin = Pin(16, Pin.OUT)

pin.toggle()

#pwm = PWM(Pin(16, Pin.OUT))

#pwm.freq(1000)

#    for duty in range(65025,1000):
    #    pwm.duty_u16(duty)
#        sleep(0.001)
 #   for duty in range(65025, 0, -1000):
  #      pwm.duty_u16(duty)
   #     sleep(0.001)