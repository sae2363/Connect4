import numpy as np
import Agents.nodeClass as node
from point import point
class node:
    parent:node#pointer up the tree
    nextNodes:list[node]#children
    state:np.array # state of borad at this node
    p1Win:int #how many times p1 won
    p2Win:int #how many times p2 won
    totalUtil:int #Util total
    isTerminal:bool #if the node has a state that is terminal 
    player:int #whos move is it
    action:point #move to get to this state


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
        self.totalUtil=0
    #unneeded 
    """def isTerminal(self,winner):
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
            current=current.parent"""
    #print method for debuging
    def calculateFraction(self):
        total=self.p1Win+self.p2Win
        if total == 0:
            return "N/A"
        p1Fraction = self.p1Win / total
        p2Fraction = self.p2Win / total
        return f"p1: {p1Fraction:.2f}, p2: {p2Fraction:.2f}"
    def __str__(self):
        return "p1 win "+str(self.p1Win)+" p2 win "+str(self.p2Win)+" "+str(self.player)
    def __repr__(self):
        return self.__str__()
    #print method for debuging
    def printTree(self, level=0):
        print("  " * level + self.calculateFraction())
        for child in self.nextNodes:
            child.printTree(level + 1)

