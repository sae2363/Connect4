from Agents.ASPtwo import StateT, ActionT,ASP
from abc import ABC
from typing import Generic
from Agents.agent import AdversarialAgent
import Agents.nodeClass as n
import numpy as np
import math,random
import time
import point

class MCTS(AdversarialAgent[StateT, ActionT], ABC):
    """A game-playing agent defining a strategy for adversarial search problems."""
    root:n.node=None
    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        return self.MCTS(state)
    def MCTS(self,state:StateT)-> ActionT:
        """
        A large and dense method whichs runs monte carlo tree search.

        :param      state       Game state
        :returns    Action chosen by the agent
        
        """
        assert not self._problem.is_terminal(
            state
        ), "MCTS expects a non-terminal state as input"
        #creates root of the tree which stores the data for MCTS
        root=n.node(state,None,self._problem.is_terminal(state),self._problem.player(state),None)

        #Time limit for the search
        startTime=time.time_ns()
        timeToDecide=int(0.5*1000000000) #time in ns for bot to run MCTS
        endTime=startTime+timeToDecide
        #used to count how many times the loop is run
        count=0
        #creates the tree with leaves consisting of all actions that are possible by the current player
        self.createTree(root.state,root,0,1)
        
        #MCTS as presented in AIMA
        while(time.time_ns()<endTime):
            #finds node with the highest UTC
            node:n.node=self.findLeafUTC(root)
            #makes a new sub node for the node with a random action
            nextNode=self.expand(node)
            #play out to the game end and returns who won
            result=self.playOut(np.copy(nextNode.state))
            #update the whole tree back up
            self.backTrack(nextNode,result)
            count+=1
        #gets the best move with the most playthroughs 
        bestActionNode=self.getBest(root)
        #get the action from that node
        return bestActionNode.action

    def printTree(self,root:n.node,max :int, level=1):
        """
        Prints the tree from the root provided to the depth level

        :param      root    the root node of the tree which stores data
                    level the depth of the tree the method is in
        
        """
        if(level>max):
            return None
        size=len(root.nextNodes)
        if(root.player==1):
            winNumber=root.p1Win
        else:
            winNumber=root.p2Win
        value=str(root.player)+" "+str(int(self.find_UCB1(root)*1000000)/1000000.0)+" "+str(root.action)+" "+str(root.p1Win)+" "+str(root.p2Win)
        print("        " * level + " "+str(value))
        for i in range(size):
            self.printTree(root.nextNodes[i],max,level + 1)

    def treeSize(self,root:n.node):
        """
        A way to find out how many nodes are in the tree from the root node

        :param      root    the root node of the tree which stores data
        :returns    how many nodes are in the tree from the root node
        
        """
        count=0
        if(len(root.nextNodes)==0):
            return 1
        for n in root.nextNodes:
            count+=self.treeSize(n)
        return count
    
    def getBest(self,root:n.node):
        """
        Gets the child of the root node provided with the larger number of playouts

        :param      root    the root node of the tree which stores data
        :returns    Returns the best child node of the root by how many total play outs happened via the node
        
        """
        maxPlay:float=-100000
        for child in root.nextNodes:
            childPlay=child.p1Win+child.p2Win
            if(childPlay>maxPlay):
                bestNode=child
                maxPlay=childPlay
        return bestNode
        
    def backTrack(self,root:n.node,winner:float):
        """
        Starting from the leave that was made in the expand method all the way to the top of the tree
        Keep iterating up the tree till it hits a node with no parent

        :param      root    a node of the tree which stores data
        :returns    None
        
        """
        current=root
        while(current!=None):
            if(winner>=0.6):
                current.p1Win+=1
            if(winner<=0.4):
                current.p2Win+=1
            current.totalUtil+=winner
            current.total+=1
            current=current.parent
            

    def playOut(self,state:np.array)->float:
        """
        Starting with the state provided,  play out till the state is terminal 

        :param      state    the current state of the board
        :returns    float    the Utility of the terminal state
        
        """
        if(self._problem.is_terminal(state)):
            return self._problem.utility(state)
        actionList=[]
        for a in self._problem.actions(state):
            actionList.append(a)
        action=random.choice(actionList)
        nextState=self._problem.result(state,action)
        return self.playOut(nextState)


    def expand(self, root:n.node)->n.node:
        """
        picks a random action from the root node and create a new node with it

        :param      root    a node of the tree which stores data
        :returns    node    the newly created node with a pointer to the root node provided
        
        """
        actionList:point.point=[]
        if(self._problem.is_terminal(root.state)):
            return root
        for a in self._problem.actions(root.state):
            actionList.append(a)
        i=0
        while (i<len(actionList)):
            value=True
            for b in root.nextNodes:
                if(actionList[i].x==b.action.x and value):
                    del actionList[i]
                    i-=1
                    value=False
            i+=1
        action=random.choice(actionList)
        nextState=self._problem.result(root.state,action)
        node=n.node(nextState,root,self._problem.is_terminal(nextState),self._problem.player(nextState),action)
        root.nextNodes.append(node)
        return node
    def createTree(self,state:np.array,root:n.node,depth:int,max:int):
        """
        Create the initial tree to be used by MCTS with a root and all possible actions of the root as leaves up to a depth

        :param      root    a node of the tree which stores data
                    state   the current state of the board
                    max     how deep the tree should be
                    depth   how deep the method is 
        :returns    node    the newly created node with a pointer to the root node provided
        
        """
        if(depth<max and not(self._problem.is_terminal(state))):
            for a in self._problem.actions(state):
                isTerm=self._problem.is_terminal(self._problem.result(state,a))
                player:int=self._problem.player(self._problem.result(state,a))
                nextNode=n.node(self._problem.result(state,a),root,isTerm,player,a)
                root.nextNodes.append(nextNode)
                self.createTree(nextNode.state,nextNode,depth+1,max)
    def findLeafUTC(self,root:n.node)->n.node:
        """
        Returns a leaf from the tree with the highest UTC value
        
        :param      root    a node of the tree which stores data
        :returns    node    the node with the highest UTC Value
        
        """
        rootUTC=-100000000
        maxUTC=-100000000
        bestNode:n.node=None
        if(len(root.nextNodes)==0):
            return root
        if(len(root.nextNodes)!=len(self._problem.actions(root.state)) and root.parent!=None):
            rootUTC=self.find_UCB1(root)
            maxUTC=rootUTC
            bestNode=root
        for child in root.nextNodes:
            childUTC=self.find_UCB1(child)
            if(childUTC>maxUTC):
                bestNode=child
                maxUTC=childUTC
        if((np.array_equal(bestNode.state,root.state) or bestNode==root)):
            return root
        if(maxUTC==0):
            bestNode=random.choice(root.nextNodes)

        return self.findLeafUTC(bestNode)



    def findRandomLeaf(self,root:n.node)->n.node:
        """
        Returns a leaf from the tree by randomly traversing the tree
        
        :param      root    a node of the tree which stores data
        :returns    node    the node chosen
        
        """
        if(len(root.nextNodes)==0):
            return root
        if(len(root.nextNodes)==len(self._problem.actions(root.state))):
            return self.findRandomLeaf(random.choice(root.nextNodes))
        number:int=int(np.random.random()*10000) % (2+len(root.nextNodes))
        if(number<=1):
            return root
        else:
            return self.findRandomLeaf(root.nextNodes[number-2])

    def find_UCB1(self,root:n.node)->float:
        """
        Returns the UTC value of the node
        
        :param      root    a node of the tree which stores data
        :returns    float   UTC Value
        
        """
        winCount=0
        if(root.player==2):
            winCount=root.p1Win
        else:
            winCount=root.p2Win
        if(root.parent==None):
            return -100
        try:
            totalUtil=root.totalUtil
            if(root.player==1):
                totalUtil=root.total-root.totalUtil
            ucb1=(totalUtil/(root.total))+ (math.sqrt(2)*math.sqrt(math.log(root.parent.total*1.0)/float(root.total)))
        except:
            ucb1=1000
        return ucb1
    

