import machine
import time
import ds18x20
import onewire

pin13 = machine.Pin(14, machine.Pin.OUT)
#pin15 = machine.Pin(15, machine.Pin.OUT)
#rcent = 0
#while True:
#    fan.duty_u16(500)
#    percent += 1000
#    time.sleep_ms(100)
    #pin15.toggle()
    #time.sleep_ms(1500)


ds = ds18x20.DS18X20(onewire.OneWire(pin13))
roms = ds.scan()
print(roms)

#while True:
#    pin13.toggle()
#    time.sleep_ms(15000)


#while True:
#    pin15.toggle()
#    time.sleep_ms(1000)

while True:
      ds.convert_temp()
      time.sleep_ms(1000)
      for rom in roms:
        temp = ds.read_temp(rom)
        print(f"Current temperature: {temp}")
        #send_data(s, temp)