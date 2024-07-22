import numpy as np
import Agents.nodeClass as node
from point import point
class node:
    parent:node
    nextNodes:list[node]
    state:np.array
    p1Win:int
    p2Win:int
    total:int
    isTerminal:bool
    player:int
    action:point

    def __init__(self,stateArray:np.array,parent,isTerm,player:int,point:point):
        self.state=stateArray
        self.p1Win=0
        self.p2Win=0
        self.total=0
        self.parent=parent
        self.nextNodes=[]
        self.isTerminal=isTerm
        self.action=point
        self.player=player
    
    def isTerminal(self,winner):
        current=self
        while(current!=None):
            if(winner==1):
                current.p1Win+=1
            if(winner==2):
                current.p2Win+=1
            current=current.parent
    def updateWinner(self,winner):
        current=self
        while(current!=None):
            if(winner==1):
                current.p1Win+=1
            if(winner==2):
                current.p2Win+=1
            current=current.parent
    def calculateFraction(self):
        total=self.p1Win+self.p2Win
        if total == 0:
            return "N/A"
        p1Fraction = self.p1Win / total
        p2Fraction = self.p2Win / total
        return f"p1: {p1Fraction:.2f}, p2: {p2Fraction:.2f}"

    def printTree(self, level=0):
        print("  " * level + self.calculateFraction())
        for child in self.nextNodes:
            child.printTree(level + 1)

