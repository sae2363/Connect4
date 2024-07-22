import tkinter as tk
from tkinter import *
import numpy as np

class GUI:
    def __init__(self, root, state):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Connect 4")

        # Below is the connect 4 board 

        gridSizeX = len(state) # Check the length of the array to know how many squares the grid needs to be
        gridSizeY = len(state[0])

        self.board = tk.Frame(root, height=300, width=300, relief='solid', borderwidth=1) # creaste a Frame object called board

        for j in range(gridSizeX): # all the columns
            self.board.grid_columnconfigure(j,  weight =1, minsize=300/gridSizeX)
            for i in range(gridSizeY): # specify how many rows and columns we will need
                self.board.grid_rowconfigure(i,  weight =1, minsize=300/gridSizeY)
                if int(state[j][i]) == 1:
                    foregroundColor = 'blue'
                elif int(state[j][i]) == 2:
                    foregroundColor = 'red'
                else: foregroundColor = 'black'
                Label(self.board, text=int(state[j][i]), foreground=foregroundColor).grid(row=i, column=j)

        self.board['relief'] = 'solid'
        self.board.grid(row=1, column=1) # Draw the board

        # Below is the code for the buttons

        self.buttonFrame = tk.Frame(root, height=20, width=300) # creaste a Frame object called board

        for i in range(gridSizeX):
            text = "^"+str(i)
            self.buttonFrame.grid_columnconfigure(i,  weight =1, minsize=300/gridSizeX)
            Button(self.buttonFrame, text=text, command=lambda button_text=text: self.on_button_click(button_text)).grid(row=gridSizeY, column=i) # assign functionality

        self.buttonFrame.grid(row=2, column=1) # Draw the button board

        # Below is the code for the AGENT BUTTONS

        self.agentFrame = tk.Frame(self.root, relief='solid', borderwidth=1).grid()

        self.agent1button = tk.Button(self.agentFrame, text='Monte Carlo Tree Search').grid()
        self.agent2button = tk.Button(self.agentFrame, text='Alpha-Beta Pruning (MINMAX)').grid()

        # EXTRA

        self.label1 = tk.Label(self.root, text="Connect 4")
        self.label1.grid(row=0, column=0)


    def on_button_click(self, column): # this function recieves the value of whatever move was selected (which button got pressed)
        column = column[1]
        self.label1 = tk.Label(root, text=(column, "Button Clicked!"))
        self.label1.grid(row=0, column=0)
        return int(column)


testState = np.zeros((5, 6))
testState[1][1] = '1'
testState[1][2] = '2'
testState[2][2] = '1'
root = tk.Tk()
app = GUI(root, state=testState)
root.mainloop()
