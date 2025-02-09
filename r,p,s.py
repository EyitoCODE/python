"""
Rock, Paper, Scissors Game
Author: [Oritse-tsegbemi Eyito]
Date: [2005-02-09]
Description: A simple Rock, Paper, Scissors game where the player competes against the CPU.
             The program ensures valid input, handles case sensitivity, and determines the winner.

Version: 1.1
Python Version: 3.13.1
"""
import random #to make the cpu's choice random

# options cpu can choose 
options = ["rock", "paper", "scissors"]
cpu_decision = random.choice(options)

def get_choices():

    player_choice = input("Choose rock, paper, or scissors\n")   #player's choice
    cpu_choice= cpu_decision      #cpu's choice
    choices= {"player": player_choice, "CPU": cpu_choice}
    
    return choices

#checks if the player or cpu wins
def check_win(player, cpu):
    print(f"You chose {player} \n CPU chose {cpu}")
    if player == cpu:
        return "It's a tie!"
    elif player == "rock": 
        if cpu == "scissors":
            return "Rock smashes scissors! You Win!"
        else:
           return "Paper covers rock! You lose."    

    elif player == "paper": 
        if cpu == "rock":
            return "Paper covers rock! You Win!"
        else:
            return "Scissors cut paper! You lose"


    elif player == "scissors": 
        if cpu == "paper":
            return "Scissors cut paper! You Win!"
        else:
            return "Rock smashes scissors! You lose"

choices = get_choices()

result = check_win(choices["player"], choices["CPU"])
print(result)

# choices = get_choices()
# print(choices)
#ok ok
