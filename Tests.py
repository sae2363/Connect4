import board as b
import Agents.alphabeta as ab
import Agents.MCTS as mc
import numpy as np
from gui import GUI
import tkinter as tk
import time
from point import point as p

'''
This file contains a test which will set up a game played by 2 alpha-beta agents against each other.
'''


def TestAB():   
    '''
    Will display the GUI and will run two alpha-beta agents playing against each other.
    '''

    g:b.board=b.board(4,4,4)

    agent1 = ab.AlphaBeta(g) # max
    agent2 = ab.AlphaBeta(g) # min

    root = tk.Tk()
    app = GUI(root)

    app.createBoard(g.array)
    root.update()

    while not g.is_terminal(g.array):

        if g.current_player(g.array) == 1:
            action1 = agent1.choose_action(g.array)
            g.placePiece(g.array, action1.x, 1)

        elif g.current_player(g.array) == 2:
            action2 = agent2.choose_action(g.array)
            g.placePiece(g.array, action2.x, 2)
        
        print(g.current_player(g.array))
        print(g.array)

        app.updateBoard(g.array)
        root.update()
        time.sleep(2)
        
    print('DONE', g.who_is_winner(g.array))
    app.display_message(f'{g.who_is_winner(g.array)} wins')
    root.update()
    root.mainloop()


def PlayAB():   
    '''
    Will display the GUI and will run an alpha-beta agent (max) playing against the player input (min).
    '''
    g:b.board=b.board(4,4,4)

    agent1 = ab.AlphaBeta(g) # max

    root = tk.Tk()
    app = GUI(root)

    app.createBoard(g.array)
    root.update()

    m = 0

    while not g.is_terminal(g.array):

        if g.current_player(g.array) == 1:
            app.display_message('AI is choosing move...')
            root.update()
            start=time.time()
            action1 = agent1.choose_action(g.array)
            timeElapsed = time.time()-start
            print(timeElapsed+' on move '+m)
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

    print('DONE', g.who_is_winner(g.array))    
    app.display_message(f'{g.who_is_winner(g.array)} wins')
    root.update()
    root.mainloop()


def TestMC():
    '''
    Will display the GUI and will run two Monte-Carlo Tree Search agents playing against each other.
    '''

    g:b.board=b.board(2,2,2)

    agent1 = mc.MCTS(g) # max
    agent2 = mc.MCTS(g) # min

    root = tk.Tk()
    app = GUI(root)

    app.createBoard(g.array)
    root.update()

    while not g.is_terminal(g.array):

        if g.current_player(g.array) == 1:
            action1 = agent1.choose_action(g.array)
            g.placePiece(g.array, action1.x, 1)

        elif g.current_player(g.array) == 2:
            action2 = agent2.choose_action(g.array)
            g.placePiece(g.array, action2.x, 2)
        
        print(g.current_player(g.array))
        print(g.array)

        app.updateBoard(g.array)
        root.update()
        time.sleep(2)
        
    print('DONE', g.who_is_winner(g.array))
    app.display_message(f'{g.who_is_winner(g.array)} wins')
    root.update()
    root.mainloop()


def PlayMC():   
    '''
    Will display the GUI and will run a Monte-Carlo Tree Search agent (max) playing against the player input (min).
    '''
    g:b.board=b.board(7,7,4)

    agent1 = mc.MCTS(g) # max

    root = tk.Tk()
    app = GUI(root)

    app.createBoard(g.array)
    root.update()

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

    print('DONE', g.who_is_winner(g.array))
    app.display_message(f'{g.who_is_winner(g.array)} wins')
    root.update()
    root.mainloop()


def TestMCvAB():
    '''
    Will display the GUI and will run a Monte-Carlo Tree Search agent playing against an Alpha-Beta agent.
    '''

    g:b.board=b.board(6,6,4)

    agent2 = ab.AlphaBeta(g) # max
    agent1 = mc.MCTS(g) # min

    root = tk.Tk()
    app = GUI(root)

    app.createBoard(g.array)
    root.update()

    while not g.is_terminal(g.array):

        if g.current_player(g.array) == 1:
            action1 = agent1.choose_action(g.array)
            g.placePiece(g.array, action1.x, 1)

        elif g.current_player(g.array) == 2:
            action2 = agent2.choose_action(g.array)
            g.placePiece(g.array, action2.x, 2)
        
        print(g.current_player(g.array))
        print(g.array)

        app.updateBoard(g.array)
        root.update()
        time.sleep(2)
        
    print('DONE', g.who_is_winner(g.array))
    app.display_message(f'{g.who_is_winner(g.array)} wins')
    root.update()
    root.mainloop()


PlayAB()
