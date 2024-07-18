import numpy as np
class point:
    x:int#colum
    y:int#row
    def __init__(self,yValue:int,xValue:int) -> None:
        self.x=xValue
        self.y=yValue
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"
    def checkVal(self,board,player):
        return board[self.y][self.x]==player 