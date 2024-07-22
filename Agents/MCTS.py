from Agents.ASPtwo import StateT, ActionT,ASP
from abc import ABC
from typing import Generic
from Agents.agent import AdversarialAgent
import Agents.nodeClass as n
import numpy as np
import math
import time

class MCTS(AdversarialAgent[StateT, ActionT], ABC):
    """A game-playing agent defining a strategy for adversarial search problems."""
    root:n.node
    def choose_action(self, state: StateT) -> ActionT:
        """Select an action for the given state using the agent's strategy.

        :param      state       Game state
        :returns    Action chosen by the agent
        """
        return self.MCTS(state)
    def MCTS(self,state:StateT)-> ActionT:
        assert not self._problem.is_terminal(
            state
        ), "MCTS expects a non-terminal state as input"
        if(root==None):
            root=n.node(state,None,self._problem.is_terminal(state),self._problem.player(state),None)

        leafList=[]
        self.makeLeafList(root,leafList)
        startTime=time.time_ns()
        endTime=startTime+1000000000
        count=0
        while(time.time_ns()<endTime):
            node:n.node=self.findLeafUTC(root)
            self.expand(node)
            result=self.playOut(node.state)
            self.backTrack(root,result)
            count+=1
        print("Number of runs "+str(count))
        bestActionNode=self.getBest(root)
        root=bestActionNode
        return bestActionNode.action

        """
        idea so far

        while loop
        make a tree with nodes to store the data up to n deep
        go to a leaf of the tree and start randomly pick moves till terminal state is reached
        with this result, go up child node till hit root and update
        pick the actions with the highest win rate
        question right now do i save the tree to use later or not
        """
    def treeSize(self,)
    def getBest(self,root:n.node):
        maxUTC=-10000
        for child in root.nextNodes:
            childUTC=self.find_UCB1(child)
            if(childUTC>maxUTC):
                bestNode=child
                maxUTC=childUTC
        return bestNode
        
    def backTrack(self,root:n.node,winner:int):
        current=root
        while(current!=None):
            if(winner==1):
                current.p1Win+=1
            if(winner==2):
                current.p2Win+=1
            current=current.parent
            

    def playOut(self,state:np.array)->float:
        if(self._problem.is_terminal(state)):
            return self._problem.utility(state)
        actionList=[]
        for a in self._problem.actions(state):
            actionList.append(a)
        action=actionList[int((np.random.random()*10000)%len(actionList))]
        nextState=self._problem.result(state,action)
        return self.playOut(nextState)


    def expand(self, root:n.node)->n.node:
        actionList=[]
        for a in self._problem.actions(root.state):
            actionList.append(a)
        action=actionList[int((np.random.random()*10000)%len(actionList))]
        nextState=self._problem.result(root.state,action)
        node=n.node(nextState,root,self._problem.is_terminal(nextState),self._problem.player(nextState),action)
        root.nextNodes.append(node)
        return node
    def createTree(self,state:np.array,root:n.node,depth:int):
        if(depth<5 and not(self._problem.is_terminal(state))):
            for a in self._problem.actions():
                isTerm=self._problem.is_terminal(self._problem.result(state,a))
                player:int=self._problem.player(self._problem.result(state,a))
                nextNode=n.node(self._problem.result(state,a),root,isTerm,player,a)
                if(isTerm):
                    nextNode.isTerminal(self._problem.who_is_winner(nextNode.state))
                root.nextNodes.append(nextNode)
                self.createTree(nextNode.state,nextNode,depth+1)
    def makeLeafList(self,root:n.node,leafList:list):
        if(len(root.nextNodes)==0):
            leafList.append(root)
        else:
            for leaf in root.nextNodes:
                self.makeLeafList(leaf,leafList)
    def findLeafUTC(self,root:n.node)->n.node:
        rootUTC=-100000000
        maxUTC=-100000000
        bestNode:n.node
        if(len(root.nextNodes)==0):
            return root
        if(len(root.nextNodes)!=self._problem.actions(root.state)):
            rootUTC=self.find_UCB1(root)
            maxUTC=rootUTC
            bestNode=root
        for child in root.nextNodes:
            childUTC=self.find_UCB1(child)
            if(childUTC>maxUTC):
                bestNode=child
                maxUTC=childUTC
        if(np.array_equal(bestNode.state,root.state) or bestNode==root):
            return root

        return self.findLeafUTC(bestNode)



    def findRandomLeaf(self,root:n.node)->n.node:
        if(len(root.nextNodes)==0):
            return root
        if(len(root.nextNodes)!=len(self._problem.actions(root.state))):
            number:int=int(np.random.random()*10000) % (2+len(root.nextNodes))
            if(number<=2):
                return root
            else:
                return self.findRandomLeaf(root)

        return self.findRandomLeaf(root)
    def find_UCB1(self,root:n.node):
        winCount=0
        if(root.parent==None):
            return 0
        if(root.player==1):
            winCount=root.p1Win
        else:
            winCount=root.p2Win
        try:
            ucb1=winCount/(root.p1Win+root.p2Win)+ math.sqrt(2)*math.sqrt(math.log(root.parent.p1Win+root.parent.p2Win)/(root.p1Win+root.p2Win))
        except:
            ucb1=0
        return ucb1
    

