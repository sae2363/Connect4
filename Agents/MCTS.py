from Agents.ASPtwo import StateT, ActionT,ASP
from abc import ABC
from typing import Generic
from Agents.agent import AdversarialAgent
import Agents.nodeClass as n
import numpy as np
import math,random
import time

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
        assert not self._problem.is_terminal(
            state
        ), "MCTS expects a non-terminal state as input"
        try:
            if(root==None):
                root=None
        except:
            root=n.node(state,None,self._problem.is_terminal(state),self._problem.player(state),None)

        leafList=[]
        self.makeLeafList(root,leafList)
        startTime=time.time_ns()
        timeToDecide=int(1*1000000000) #time in ns for bot to run MCTS
        endTime=startTime+timeToDecide
        count=0
        self.createTree(root.state,root,0,1)
        while(time.time_ns()<endTime):
            node:n.node=self.findLeafUTC(root)
            nextNode=self.expand(node)
            result=self.playOut(np.copy(nextNode.state))
            #print(result)
            self.backTrack(nextNode,result)
            count+=1
        #print("tree")
        #self.printTree(root,3)
        print("")
        print("Number of runs "+str(count))
        print("tree Size "+str(self.treeSize(root)))
        bestActionNode=self.getBest(root)
        #root=bestActionNode
        #print
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
    def printTree(self,root:n.node,max :int, level=1):
        if(level>max):
            return None
        size=len(root.nextNodes)
        #for i in range(int(size/2)):
        #    self.printTree(root.nextNodes[i],level + 1)
        if(root.player==1):
            winNumber=root.p1Win
        else:
            winNumber=root.p2Win
        print("       " * level + " "+str((int(((winNumber/(root.p1Win+root.p2Win))*1000))/1000.0)))
        for i in range(size):#int(size/2)):
            self.printTree(root.nextNodes[i],max,level + 1)#math.ceil(size/2)+i

    def treeSize(self,root:n.node):
        count=0
        if(len(root.nextNodes)==0):
            return 1
        for n in root.nextNodes:
            count+=self.treeSize(n)
        return count
    def getBest(self,root:n.node):
        """maxUTC:float=-10000
        for child in root.nextNodes:
            childUTC=self.find_UCB1(child)
            if(childUTC>maxUTC):
                bestNode=child
                maxUTC=childUTC"""
        #print("max UTC "+str(maxUTC))
        maxPlay:float=-10000
        for child in root.nextNodes:
            childPlay=child.p1Win+child.p2Win
            if(childPlay>maxPlay):
                bestNode=child
                maxPlay=childPlay
            #print(str(child.action)+"  "+str(child.p1Win+child.p2Win)+"  "+str(self.find_UCB1(child)))
        return bestNode
        
    def backTrack(self,root:n.node,winner:float):
        current=root
        while(current!=None):
            #if(current.player==1):
            if(winner<=0.6 and winner>=0.4):
                current.p1Win+=1
                current.p2Win+=1
            if(winner>=0.6):
                current.p1Win+=1
            if(winner<=0.4):
                current.p2Win+=1
            current=current.parent
            

    def playOut(self,state:np.array)->float:
        if(self._problem.is_terminal(state)):
            return self._problem.utility(state)
        actionList=[]
        for a in self._problem.actions(state):
            actionList.append(a)
        #print([str(item) for item in actionList])
        action=random.choice(actionList)
        nextState=self._problem.result(state,action)
        return self.playOut(nextState)


    def expand(self, root:n.node)->n.node:
        actionList=[]
        if(self._problem.is_terminal(root.state)):
            return root
        for a in self._problem.actions(root.state):
            actionList.append(a)
        #try to remove dupe,  change the first one to a while loop
        i=0
        #print("before")
        """s=""
        s2=""
        for a in actionList:
            s+= str(a)+"  "
        print(s)
        for b in root.nextNodes:
            s2+= str(b)+"  "
        print("action list")
        print(s)
        print("next nodes list")
        print(s2)"""
        s=""
        value=True
        while (i<len(actionList)):
            for b in root.nextNodes:
                if(actionList[i].x==b.action.x and actionList[i].y==b.action.y and value):
                    del actionList[i]
                    i-=1
                    value=False
            i+=1
        #print("after")
        for a in actionList:
            s+= str(a)+"  "
        #print(s)
        action=random.choice(actionList)
        nextState=self._problem.result(root.state,action)
        node=n.node(nextState,root,self._problem.is_terminal(nextState),self._problem.player(nextState),action)
        root.nextNodes.append(node)
        return node
    def createTree(self,state:np.array,root:n.node,depth:int,max:int):
        if(depth<max and not(self._problem.is_terminal(state))):
            for a in self._problem.actions(state):
                isTerm=self._problem.is_terminal(self._problem.result(state,a))
                player:int=self._problem.player(self._problem.result(state,a))
                nextNode=n.node(self._problem.result(state,a),root,isTerm,player,a)
                
                root.nextNodes.append(nextNode)
                self.createTree(nextNode.state,nextNode,depth+1,max)
    def makeLeafList(self,root:n.node,leafList:list):
        if(len(root.nextNodes)==0):
            leafList.append(root)
        else:
            for leaf in root.nextNodes:
                self.makeLeafList(leaf,leafList)
    def findLeafUTC(self,root:n.node)->n.node:
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
        #print("max utc "+str(maxUTC))
        if((np.array_equal(bestNode.state,root.state) or bestNode==root)):
            return root
        if(maxUTC==0):
            bestNode=random.choice(root.nextNodes)

        return self.findLeafUTC(bestNode)



    def findRandomLeaf(self,root:n.node)->n.node:
        if(len(root.nextNodes)==0):
            return root
        if(len(root.nextNodes)==len(self._problem.actions(root.state))):
            return self.findRandomLeaf(random.choice(root.nextNodes))
        #if(len(root.nextNodes)!=len(self._problem.actions(root.state))):
        number:int=int(np.random.random()*10000) % (2+len(root.nextNodes))
        if(number<=1):
            return root
        else:
            return self.findRandomLeaf(root.nextNodes[number-2])

        #return self.findRandomLeaf(root)
    def find_UCB1(self,root:n.node)->float:
        winCount=0
        if(root.player==2):
            winCount=root.p1Win
        else:
            winCount=root.p2Win
        if(root.parent==None):
            try:
                return -100
            except:
                return -100 
        try:
            ucb1=winCount/(root.p1Win+root.p2Win)+ math.sqrt(2)*math.sqrt(math.log(root.parent.p1Win+root.parent.p2Win)/(root.p1Win+root.p2Win))
        except:
            ucb1=1000
        return ucb1
    

