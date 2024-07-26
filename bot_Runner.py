from board import board as b
import Agents.MCTS as mc
from Agents.randomAgent import randomAgent as ra
import numpy as np
from Agents.realAgent import realAgent as rl
from Agents.alphabeta import AlphaBeta as ab
import time as ti
#run a command line based version of the game 
def runCLI():
    """Run the game in the command line"""
    row=None
    col=None
    win=None
    typeOfBot=None
    while row is None:
        user_input = input("Please input your desired row size (e.g., 3): ").strip()

        try:
            row = int(user_input)
        except ValueError as e:
            print(f"{e}\nCannot parse given number. Please try again...\n")
    while col is None:
        user_input = input("Please input your desired colum size (e.g., 3): ").strip()

        try:
            col = int(user_input)
        except ValueError as e:
            print(f"{e}\nCannot parse given number. Please try again...\n")
    while win is None:
        user_input = input("Please input your desired number in a row to win (e.g., 3): ").strip()

        try:
            win = int(user_input)
        except ValueError as e:
            print(f"{e}\nCannot parse given number. Please try again...\n")
    while typeOfBot is None:
        user_input = input("Please input your desired bot to verse \n0 monte carlo tree search\n1 Alpha Beta\n2 Random ").strip()

        try:
            typeOfBot = int(user_input)
        except ValueError as e:
            print(f"{e}\nCannot parse given number. Please try again...\n")
    game:b=b(row,col,win)
    #player_a = rl(game)
    match typeOfBot:
      case 0:
        player_b = mc.MCTS(game)
      case 1:
        player_b = ab(game)
      case 2:
        player_b = ra(game)

    i=0
    while(not(game.is_terminal(game.array))):
        print(game.array)
        if(i%2==0):

            user_input = input("Please input your colum to place piece in (e.g., 0): ").strip()
            try:
                game.placePiece(game.array,int(user_input),1)
            except ValueError as e:
                print(f"{e}\nCannot parse given value. Please try again...\n")
            i+=1
        else:
            temp=player_b.choose_action(game.array)
            game.placePiece(game.array,temp.x,2)
            i+=1
    winner=game.who_is_winner(game.array)
    print("winning board")
    print(game.array)
    match winner:
      case 0:
        print("Its a draw")
      case 1:
        print("Player one wins")
      case 2:
        print("Player two wins")

row=4
col=4
winBy=3

def runBotUTC():
  
  game:b=b(col,row,winBy)
  player_a = mc.MCTS(game)
  player_b = mc.MCTS(game)
  return runBots(game,player_a,player_b)

def runBotUTC_Ran():
  game:b=b(col,row,winBy)
  player_b = mc.MCTS(game)
  player_a = ra(game)
  """player_a = mc.MCTS(game)
  player_b = ra(game)"""
  return runBots(game,player_a,player_b)

def runBotUTC_ab():
  game:b=b(col,row,winBy)
  player_b = mc.MCTS(game)
  player_a = ab(game)
  """player_a = mc.MCTS(game)
  player_b = ab(game)"""
  return runBots(game,player_a,player_b)

def runBotab_ran():
  game:b=b(col,row,winBy)
  player_a = ra(game)
  player_b = ab(game)
  """player_a = ab(game)
  player_b = ra(game)"""
  return runBots(game,player_a,player_b)
def runBotab_MCTS_Time():
  game:b=b(col,row,winBy)
  player_b = ab(game)
  player_a = mc.MCTS(game)
  """player_a = ab(game)
  player_b = mc.MCTS(game)"""
  return runBotsWithTime(game,player_a,player_b)
def runBotMCTS_MCTS_Time():
  game:b=b(col,row,winBy)
  player_a = mc.MCTS(game)
  player_b = mc.MCTS(game)
  return runBotsWithTime(game,player_a,player_b)
   

def runBots(game,player_a,player_b):
  """Run the 2 agents provided verse each other"""
  i=0
  while(not(game.is_terminal(game.array))):
      #print(game.array)
      if(i%2==0):
          #print("p1")
          temp=player_a.choose_action(np.copy(game.array))
          game.placePiece(game.array,temp.x,1)
          i+=1
      else:
          #print("p2")
          temp2=player_b.choose_action(np.copy(game.array))
          game.placePiece(game.array,temp2.x,2)
          i+=1
  winner=game.who_is_winner(game.array)
  print(game.array)
  match winner:
    case 0:
      print("Its a draw")
      return 0
    case 1:
      print("Player one wins")
      return 1
    case 2:
      print("Player two wins")
      return 2
def runBotsWithTime(game,player_a,player_b):
  """Run the 2 agents provided verse each other"""
  i=0
  #time List
  t=[]
  while(not(game.is_terminal(game.array))):
      if(i%2==0):
          start=ti.time()
          temp=player_a.choose_action(np.copy(game.array))
          game.placePiece(game.array,temp.x,1)
          i+=1
          t.append(ti.time()-start)
      else:
          start=ti.time()
          temp2=player_b.choose_action(np.copy(game.array))
          game.placePiece(game.array,temp2.x,2)
          i+=1
          t.append(ti.time()-start)
  winner=game.who_is_winner(game.array)
  print(game.array)
  match winner:
    case 0:
      print("Its a draw")
      return 0,t
    case 1:
      print("Player one wins")
      return 1,t
    case 2:
      print("Player two wins")
      return 2,t
