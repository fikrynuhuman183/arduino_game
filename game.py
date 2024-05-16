# import modules from Pyfirmata
from pyfirmata import Arduino, util, INPUT, OUTPUT 
# import inbuilt time module
import time
from random import randint
import numpy as np

# create an Arduino board instance
board = Arduino ("COM7")
# digital pin number

#Led and button for start/end game
game_run_led = board.digital[3]
game_run_led.mode = OUTPUT

#button start/end
btn_start_end = board.analog[5]
btn_start_end.mode = INPUT
prev_state_btn_start_end = 0

#piezo buzzer
buzzer = board.digital[4]


#Decision Matrix
decision_matrix = [[0.5,0,1,0,1],
                   [1,0.5,0,1,0],
                   [0,1,0.5,0,1],
                   [1,0,1,0.5,0],
                   [0,1,0,1,0,0.5]]



#Leds representing computer choice
com_choice_0 = board.digital[7]
com_choice_1 = board.digital[6]
com_choice_2 = board.digital[5]

com_choice_0.mode = OUTPUT
com_choice_1.mode = OUTPUT
com_choice_2.mode = OUTPUT

com_choice_leds = [com_choice_0,com_choice_1,com_choice_2]

#Leds representing computer score
com_score_0 = board.digital[10]
com_score_1 = board.digital[9]
com_score_2 = board.digital[8]

com_score_0.mode = OUTPUT
com_score_1.mode = OUTPUT
com_score_2.mode = OUTPUT

com_score_leds = [com_score_0,com_score_1,com_score_2]

#Leds representing user score
user_score_0 = board.digital[13]
user_score_1 = board.digital[12]
user_score_2 = board.digital[11]

user_score_0.mode = OUTPUT
user_score_1.mode = OUTPUT
user_score_2.mode = OUTPUT

user_score_leds = [user_score_0,user_score_1,user_score_2]

#buttons for user input
btn_user_choice_0 = board.analog[0]
btn_user_choice_1 = board.analog[1]
btn_user_choice_2 = board.analog[2]
btn_user_choice_3 = board.analog[3]
btn_user_choice_4 = board.analog[4]

btn_user_choice_0.mode = INPUT
btn_user_choice_1.mode = INPUT
btn_user_choice_2.mode = INPUT
btn_user_choice_3.mode = INPUT
btn_user_choice_4.mode = INPUT




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

    
    time.sleep(3)
    
    
    

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
    print('Enter your choice')
    while True:
       
        if(choice != -1 or (time.time() - start_time) > 10):
            break        
        if (btn_user_choice_0.read() and btn_user_choice_0.read() > 0.8):
            choice = 0
        elif (btn_user_choice_1.read() and btn_user_choice_1.read() > 0.8):
            choice = 1
        elif (btn_user_choice_2.read() and btn_user_choice_2.read() > 0.8):
            choice = 2
        elif (btn_user_choice_3.read() and btn_user_choice_3.read() > 0.8):
            choice = 3
        elif (btn_user_choice_4.read() and btn_user_choice_4.read() > 0.8):
            choice = 4
        time.sleep(0.01)
    game_run_led.write(0)
    return choice

def display_score(com_score, user_score):
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


start_game()

while round <7:
    buzzer.write(1)
    time.sleep(1)
    buzzer.write(0)

    user_choice = get_user_input()
    time.sleep(2)
    if user_choice == -1:
        round +=1
        com_score +=1
        display_score(com_score, user_score)
        continue
    
    com_choice = get_com_choice()

    winner = choose_winner(com_choice, user_choice)

    if winner ==1 :   
        user_score += 1
    elif winner == 0 :
        com_score += 1


    
    display_score(com_score, user_score, round)
    
    time.sleep(2)
    round +=1

end_game()

    


        



