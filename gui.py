import tkinter as tk
from tkinter import *
import numpy as np

class GUI:

    def __init__(self, root):

        self.root = root
        self.root.geometry("500x500")
        self.root.title("Connect 4")
        self.label1 = tk.Label(self.root)
        self.label2 = tk.Label(self.root)
        

    def createBoard(self, state):
      
        self.updateBoard(state)

        # Below is the code for the buttons
        
        gridSizeX = len(state) # Check the length of the array to know how many squares the grid needs to be
        gridSizeY = len(state[0])

        self.buttonFrame = tk.Frame(self.root, height=20, width=300) # creaste a Frame object called board

        for i in range(gridSizeX):
            text = "^"+str(i)
            self.buttonFrame.grid_columnconfigure(i,  weight =1, minsize=300/gridSizeX)
            Button(self.buttonFrame, text=text, command=lambda button_text=text: self.on_button_click(button_text)).grid(row=gridSizeY, column=i) # assign functionality

        self.buttonFrame.grid(row=2, column=1) # Draw the button board


    def updateBoard(self, state):
        
        # Below is the connect 4 board 

        gridSizeX = len(state[0]) # Check the length of the array to know how many squares the grid needs to be
        gridSizeY = len(state)

        self.board = tk.Frame(self.root, height=300, width=300, relief='solid', borderwidth=1) # creaste a Frame object called board

        for j in range(gridSizeX): # all the columns
            self.board.grid_columnconfigure(j,  weight =1, minsize=300/gridSizeX)
            for i in range(gridSizeY): # specify how many rows and columns we will need
                self.board.grid_rowconfigure(i,  weight =1, minsize=300/gridSizeY)
                if int(state[j][i]) == 1:
                    foregroundColor = 'blue'
                elif int(state[j][i]) == 2:
                    foregroundColor = 'red'
                else: foregroundColor = 'black'
                Label(self.board, text=int(state[j][i]), foreground=foregroundColor, bg=foregroundColor).grid(row=j, column=i)

        self.board['relief'] = 'solid'
        self.board.grid(row=1, column=1) # Draw the board


    def on_button_click(self, column): # this function recieves the value of whatever move was selected (which button got pressed)
        column = column[1]
        self.label2 = tk.Label(self.root, text=(column))
        self.label2.grid(row=0, column=1)
        return column

    def act(self):
        act = self.label2.cget('text')
        self.label2 = tk.Label(self.root)
        return act
    
    def display_message(self, message):
        self.label1.config(text=message)
        self.label1.grid(row=4, column=2)
        

'''
testState = np.zeros((6, 8))
testState[1][1] = '1'
testState[1][2] = '2'
testState[2][2] = '1'
root = tk.Tk()
app = GUI(root)
app.createBoard(state=testState)

root.mainloop()'''
