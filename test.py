# import modules from Pyfirmata
from pyfirmata import Arduino, OUTPUT, INPUT, util
# import inbuilt time module
import time

# create an Arduino board instance
board = Arduino ("COM6")
# digital pin number
led_pin = 0

# set it as an output pin
# board.digital[led_pin].mode = INPUT

A0_as_digital = board.analog[4]
led = board.digital[4]

# blink the LED
it = util. Iterator( board )
it.start()
A0_as_digital.enable_reporting()


while True :
 led.write(1)
#  print("READ VALUE")
    # board.digital[led_pin].write(1)
 ldr_val = A0_as_digital.read()
 print('Analog value :', ldr_val)
 time.sleep (1) 
 led.write(0)
