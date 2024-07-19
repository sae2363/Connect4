import numpy as np
class node:
    parent:
    state:np.array
    p1Win:int
    p2Win:int
    total:int

    def __init__(self,stateArray:np.array):
        self.state=stateArray
        self.p1Win=0
        self.p2Win=0
        self.total=0
