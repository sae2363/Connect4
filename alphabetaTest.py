import board as b
import Agents.alphabeta as ab
import numpy as np
from gui import GUI
import tkinter as tk
import time

def Test():   

    g:b.board=b.board(4,3)

    agent1 = ab.AlphaBeta(g) # max
    agent2 = ab.AlphaBeta(g) # min

    g.placePiece(g.array, 0, 1)

    root = tk.Tk()
    app = GUI(root)

    app.createBoard(g.array)

    while not g.is_terminal(g.array):

        if g.current_player(g.array) == 1:
            action1 = agent1.choose_action(g.array, 1)
            g.placePiece(g.array, action1.x, 1)

        elif g.current_player(g.array) == 2:
            action2 = agent2.choose_action(g.array, 2)
            g.placePiece(g.array, action2.x, 2)
        
        print(g.current_player(g.array))
        print(g.array)

        app.updateBoard(g.array)
        root.update()
        time.sleep(2)
        
    print('DONE', g.who_is_winner(g.array))

    root.mainloop()

Test()
