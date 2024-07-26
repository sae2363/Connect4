#Start the code from here
import board as b
import Agents.alphabeta as ab
import Agents.MCTS as mc
import Agents.randomAgent as ra
import numpy as np
from gui import GUI
import tkinter as tk
import time
from point import point as p
"""
Notes: p1 is max and p2 is min 
"""
def start():

    # NOTE: If using Alpha-Beta, we do not recommend anything over 4x4, as the processing times are very long.
    board_size = 4
    pieces_in_a_row = 4

    g:b.board=b.board(board_size,board_size,pieces_in_a_row)

    # ab.AlphaBeta(g) or mc.MCTS(g) or ra.randomAgent(g) or 'real'
    agent1 = ab.AlphaBeta(g) # BLUE 
    agent2 = 'real' # RED



    root = tk.Tk()
    app = GUI(root)
    
    app.createBoard(g.array)
    root.update()

    if agent1 == 'real' and agent2 == 'real':
        while not g.is_terminal(g.array):

            if g.current_player(g.array) == 1:
                app.display_message("Player 1 turn")
                root.update()
                action2 = app.act()
                action2 = p(0, action2)
                legal_actions = g.actions(g.array)
                move_strings = [point.__str__() for point in legal_actions]
                if str(action2) in move_strings:
                    g.placePiece(g.array, int(action2.x), 1)

            elif g.current_player(g.array) == 2:
                app.display_message("Player 2 turn")
                root.update()
                action2 = app.act()
                action2 = p(0, action2)
                legal_actions = g.actions(g.array)
                move_strings = [point.__str__() for point in legal_actions]
                if str(action2) in move_strings:
                    g.placePiece(g.array, int(action2.x), 2)

            app.updateBoard(g.array)
            root.update()
            time.sleep(1)

    elif agent1 == 'real':
        while not g.is_terminal(g.array):

            if g.current_player(g.array) == 2:
                app.display_message('AI is choosing move...')
                root.update()
                action1 = agent1.choose_action(g.array)
                g.placePiece(g.array, action1.x, 2)

            elif g.current_player(g.array) == 1:
                app.display_message("Player's turn")
                root.update()
                action2 = app.act()
                action2 = p(0, action2)
                legal_actions = g.actions(g.array)
                move_strings = [point.__str__() for point in legal_actions]
                if str(action2) in move_strings:
                    g.placePiece(g.array, int(action2.x), 1)

            app.updateBoard(g.array)
            root.update()
            time.sleep(1)

    elif agent2 == 'real':
        while not g.is_terminal(g.array):

            if g.current_player(g.array) == 1:
                app.display_message('AI is choosing move...')
                root.update()
                action1 = agent1.choose_action(g.array)
                g.placePiece(g.array, action1.x, 1)

            elif g.current_player(g.array) == 2:
                app.display_message("Player's turn")
                root.update()
                action2 = app.act()
                action2 = p(0, action2)
                legal_actions = g.actions(g.array)
                move_strings = [point.__str__() for point in legal_actions]
                if str(action2) in move_strings:
                    g.placePiece(g.array, int(action2.x), 2)

            app.updateBoard(g.array)
            root.update()
            time.sleep(1)
    
    else:
        while not g.is_terminal(g.array):

            if g.current_player(g.array) == 1:
                action1 = agent1.choose_action(g.array)
                g.placePiece(g.array, action1.x, 1)

            elif g.current_player(g.array) == 2:
                action2 = agent2.choose_action(g.array)
                g.placePiece(g.array, action2.x, 2)

            app.updateBoard(g.array)
            root.update()
            time.sleep(2)
            
    print('DONE', g.who_is_winner(g.array))
    app.display_message(f'{int(g.who_is_winner(g.array))} wins')
    root.update()
    root.mainloop()

def test():
    #to be able to run via pytest
    start()

if __name__ == '__main__':
    start()



    