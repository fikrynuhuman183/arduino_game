# import modules from Pyfirmata
from pyfirmata import Arduino, util, INPUT, OUTPUT 
# import inbuilt time module
import time
from random import randint
import numpy as np

# create an Arduino board instance
board = Arduino ("COM6")
# digital pin number

#Led and button for start/end game
game_run_led = board.get_pin('d:4:o')

#button start/end
btn_start_end = board.get_pin('a:5:i')
prev_state_btn_start_end = 0

#piezo buzzer
buzzer = board.get_pin('d:3:p')



#Decision Matrix
decision_matrix = [[0.5,0,1,0,1],
                   [1,0.5,0,1,0],
                   [0,1,0.5,0,1],
                   [1,0,1,0.5,0],
                   [0,1,0,1,0,0.5]]



#Leds representing computer choice
com_choice_0 = board.get_pin('d:7:o')
com_choice_1 = board.get_pin('d:6:o')
com_choice_2 = board.get_pin('d:5:o')

com_choice_leds = [com_choice_0,com_choice_1,com_choice_2]

#Leds representing computer score
com_score_0 = board.get_pin('d:10:o')
com_score_1 = board.get_pin('d:9:o')
com_score_2 = board.get_pin('d:8:o')

com_score_leds = [com_score_0,com_score_1,com_score_2]

#Leds representing user score
user_score_0 = board.get_pin('d:13:o')
user_score_1 = board.get_pin('d:12:o')
user_score_2 = board.get_pin('d:11:o')

user_score_leds = [user_score_0,user_score_1,user_score_2]

#buttons for user input
btn_user_choice_0 = board.get_pin('a:0:i')
btn_user_choice_1 = board.get_pin('a:1:i')
btn_user_choice_2 = board.get_pin('a:2:i')
btn_user_choice_3 = board.get_pin('a:3:i')
btn_user_choice_4 = board.get_pin('a:4:i')







def start_game():
    #set the intial values
    round = 0
    user_score = 0
    com_score = 0
    com_choice = -1
    user_choice = -1
    it.start()   

    btn_user_choice_0.enable_reporting()
    btn_user_choice_1.enable_reporting()
    btn_user_choice_2.enable_reporting()
    btn_user_choice_3.enable_reporting()
    btn_user_choice_4.enable_reporting()
    btn_start_end.enable_reporting()

    """ while int(btn_start_end.read()) != prev_value:
        time.sleep(0.1) """

    buzzer.write(0)
    time.sleep(2)
    
    
    

def end_game():    

    game_run_led.write(1)
    for i in range(3):
        com_score_leds[i].write(0)
        user_score_leds[i].write(0)
    
    game_run_led.write(0)
    while True:
        for led in com_choice_leds:
            buzzer.write(1)
            led.write(1)
        time.sleep(0.2)
        for led in com_choice_leds:
            buzzer.write(0)
            led.write(0)
        time.sleep(0.2)
    
    


def choose_winner(com_choice, user_choice):
    return decision_matrix[user_choice][com_choice]

def get_com_choice():
    
    com_choice = randint(0,4)
    com_choice_bin = np.binary_repr((com_choice+1),width=3)
    
    for i in range(3):
        if com_choice_bin[i]=="1":
            com_choice_leds[i].write(1)
        else:
            com_choice_leds[i].write(0)
    
    time.sleep(3)

    for led in com_choice_leds:
        led.write(0)
    
    return com_choice

def get_user_input():
    game_run_led.write(1)
    start_time = time.time()
    choice = -1
    # print('Enter your choice')
    print(btn_user_choice_1.read())
    while True:
        
        if(choice != -1 or (time.time() - start_time) > 10):
            break        
        if (btn_user_choice_0.read() and btn_user_choice_0.read() > 0.5):
            choice = 0
        elif (btn_user_choice_1.read() and btn_user_choice_1.read() > 0.5):
            choice = 1
        elif (btn_user_choice_2.read() and btn_user_choice_2.read() > 0.5):
            choice = 2
        elif (btn_user_choice_3.read() and btn_user_choice_3.read() > 0.5):
            choice = 3
        elif (btn_user_choice_4.read() and btn_user_choice_4.read() > 0.5):
            choice = 4
        time.sleep(0.01)
    game_run_led.write(0)
    return choice

def display_score(com_score, user_score, round):
    com_score_bin = np.binary_repr(com_score, width=3)
    
    user_score_bin = np.binary_repr(user_score, width=3)
    
    print(f"--------Score After Round {round+1}--------")
    print(f"Player : {user_score}")
    print(f"Computer : {com_score}")

    for i in range(3):
        if com_score_bin[i]=="1":
            com_score_leds[i].write(1)
        else:
            com_score_leds[i].write(0)
    
        if user_score_bin[i]=="1":
            user_score_leds[i].write(1)
        else:
            user_score_leds[i].write(0)
        


round = 0
user_score = 0
com_score = 0
com_choice = -1
user_choice = -1
it = util. Iterator( board )
prev_value = 0

start_game()



while round <7:
    
    buzzer.write(1)
    time.sleep(1)
    buzzer.write(0)

    user_choice = get_user_input()
    time.sleep(2)

    if user_choice == -1:
        
        com_score +=1
        display_score(com_score, user_score, round)
        round +=1
        continue
    
    com_choice = get_com_choice()
    print(user_choice)
    print(com_choice)
    winner = choose_winner(com_choice, user_choice)

    if winner ==1 :   
        user_score += 1
    elif winner == 0 :
        com_score += 1


    
    display_score(com_score, user_score, round)
    
    time.sleep(2)
    round +=1

end_game()

    


        



