from board import board as b
import Agents.MCTS as mc
import numpy as np
from Agents.realAgent import realAgent as rl

def runCLI():
    board_size=None
    while board_size is None:
        user_input = input("Please input your desired board size (e.g., 3): ").strip()

        try:
            board_size = int(user_input)
        except ValueError as e:
            print(f"{e}\nCannot parse given board size. Please try again...\n")

    game:b=b(board_size,board_size)
    player_a = rl(game)
    player_b = mc.MCTS(game)
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
    match winner:
      case 0:
        print("Its a draw")
      case 1:
        print("Player one wins")
      case 2:
        print("Player two wins")

def runBotUTC(x,y):
  game:b=b(5,4)
  player_a = mc.MCTS(game)
  player_b = mc.MCTS(game)
  return runBots(game,player_a,player_b)

def runBots(game,player_a,player_b):
  i=0
  while(not(game.is_terminal(game.array))):
      print(game.array)
      if(i%2==0):
          temp=player_a.choose_action(np.copy(game.array))
          game.placePiece(game.array,temp.x,1)
          i+=1
      else:
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
