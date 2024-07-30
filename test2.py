# import modules from Pyfirmata
from pyfirmata import Arduino, util, INPUT, OUTPUT 
# import inbuilt time module
import time
from random import randint
import numpy as np

# create an Arduino board instance
board = Arduino ("COM6")


btn_user_choice_0 = board.get_pin('a:0:i')
btn_user_choice_1 = board.get_pin('a:1:i')
btn_user_choice_2 = board.get_pin('a:2:i')
btn_user_choice_3 = board.get_pin('a:3:i')
btn_user_choice_4 = board.get_pin('a:4:i')

btn_user_choice_0.enable_reporting()
btn_user_choice_1.enable_reporting()
btn_user_choice_2.enable_reporting()
btn_user_choice_3.enable_reporting()
btn_user_choice_4.enable_reporting()

it = util. Iterator( board )

it.start()
while(True):
    print(btn_user_choice_0.read())
    print(btn_user_choice_1.read())
    
    print(btn_user_choice_2.read())
    print(btn_user_choice_3.read())
    print(btn_user_choice_4.read())
    print('\n')
    time.sleep(1)

