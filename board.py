import numpy as np
import point as p
from ASP import ASP
from numpy.typing import NDArray
class board(ASP[NDArray[np.int32], p.point]):
  #stores the game board data
  array:np.array
  #number in a row to win
  inARow:int
  #list defining the order the pieces were placed in
  pieceOrder:list
  def __init__(self,size:int,inARowToWin:int):
    """
    The method creates the connect 4 board

    Parameters
    ----------
    size : int
        the length of the x and y of the board
    inARow : int
        the number of pieces in a row needed in order to win

    Returns
    -------
    none

    Examples
    --------
    >>>
    """
    self.array = np.zeros((size, size))
    self.inARow=inARowToWin
    self.pieceOrder=[]

  def placePiece(self,state:np.array,colum:int,player:int)-> bool:
    """
    The method places a piece on the board at the colum provided and accounts for gravity 

    Parameters
    ----------
    colum : int
        the colum of the board to place in.  Indexing is 0 based and goes left to right
    player : int
        the number the player is.  Starts at 1 and goes up. (zero represents a empty space)

    Returns
    -------
    returns true or false based on how successful the placing of the piece is
            if it returns false then the colum is full
    """
    if(state[0][colum]!=0):
      return False
    i=0
    while(i<state.shape[0] and state[i][colum]==0):
      i+=1
    state[i-1][colum]=player
    self.pieceOrder.append(p.point(i-1,colum))
    return True

  def checkColum(self,state:np.array,c:int)->bool:
    return state[0][c]

  def checkLastWin(self,state:np.array,player:int)->bool:
    """
    The method determines if there is a winner for the game by checking the last placed piece by the player

    Parameters
    ----------
    state : np.array
      The 2d array representing the game board
    player : int
      the number the player is.  Starts at 1 and goes up. (zero represents a empty space)

    Returns
    -------
      Returns true or false if the player indicated won
    """
    return self.checkWin(state,player,self.pieceOrder[-1])
  def checkWin(self,state:np.array,player:int,start:p.point)-> bool:
    """
    The method determines if there is a winner for the game by checking the point provided by the player

    Parameters
    ----------
    state : np.array
      The 2d array representing the game board
    player : int
      the number the player is.  Starts at 1 and goes up. (zero represents a empty space)
    start : p.point
      the coordinates of the point to be checked

    Returns
    -------
      Returns true or false if the player indicated won
    """
    center:p.point=start
    refPoint:p.point=p.point(center.x,center.y)
    for i in range(-1,2):
     for j in range(-1,2):
      refPoint.x=center.x+(j)
      refPoint.y=center.y+(i)
      if(refPoint.x<state.shape[1] and refPoint.y<state.shape[0] 
      and refPoint.checkVal(state,player) and center.checkVal(state,player)):
        if((1+self.checkWinHelper(state,center,j,i,player,1)+self.checkWinHelper(state,center,-j,-i,player,1))>=self.inARow):
          return True

    return False
  def checkWinHelper(self,state:np.array,center:p.point,x:int,y:int,player:int,d:int)-> int:
    """
    The method is a recursive helper method to check the pieces linearly to see if someone won

    Parameters
    ----------
    center : point
      the center point for reference when checking. The code will start here and head outwards from this point
    x : int
      the direction on the x axis being checked.  -1=left, 0 = x is unchanged , 1=right
    y : int
      the direction on the y axis being checked.  -1=up, 0 = x is unchanged , 1=down
    player : int
      the number the player is.  Starts at 1 and goes up. (zero represents a empty space)
    d : int
      the distance from the center point being checked
    Returns
    -------
      Returns how many in a row of a players piece there is 
    """
    if(x==0 and y==0):
      return 0
    #center point is taken and from there a new point is made d distance and x,y direction from center
    point2:p.point=p.point((center.y+(y*d)),(center.x+(x*d)))
    #in shape row is 0, colum is 1
    #if statement checks if it is in the array bounds
    if(point2.x<state.shape[0] and point2.y<state.shape[1] and point2.x>=0 and point2.y>=0):
      #once it hits a point that is not the player then backtrack
      if(not(point2.checkVal(state,player))):
        return 0
      else:
        return 1+self.checkWinHelper(state,center,x,y,player,(d+1))
    return 0
  #Use this function for get the array to be used somewhere else
  def getBoard(self):
    """
    The method is a get method to read the data of the board

    Returns
    -------
      Returns the numpy array that is used for the board
    """
    return self.array
  def getValueOfPoint(self,row:int,colum:int):
    """
    The method is a get method to read the data of the board

    Parameters
    ----------
    row : int 
      the row of the item being checked
    colum : int
      the colum of the item being checked

    Returns
    -------
      Returns the numpy array that is used for the board
    """
    return self.array[row][colum]
  
  #Code below is methods to be used by the avd search algorithms 
  #Note: State is just the board object 
  def initial_state(self)-> np.array:
    """Generate the state representing the game's initial setup.

        The connect4 board is represented using an N x N NumPy array.

        :Parameters  state:  A numpy array that represents the board
        :returns    Initial state of the game as a 2d array
    """

    return np.zeros(self.array.shape[0],self.array.shape[0])
  
  def current_player_board(self)-> int:
    """
    Find which player has the move in the current state of the board object.

      Player "1" goes first (MAX), then "2" (MIN), etc.

      :returns    Player whose turn it is to move
    """
    if(self.array.shape[0]==0):
      return 0
    return self.array[self.pieceOrder[-1].y][self.pieceOrder[-1].x]
  
  def player(self, state: np.array) -> int:
    return self.current_player(state)
  def current_player(self,state:np.array)-> int:
    """
    Find which player has the move in the current state of the board object.

      Player "1" goes first (MAX), then "2" (MIN), etc.

      :returns    Player whose turn it is to move
    """
    if(state.shape[0]==0):
      return 0
    p1=0
    p2=0
    for i in range(state.shape[0]):
      for j in range(state.shape[1]):
        if(state[i][j]==1):
          p1+=1
        if(state[i][j]==2):
          p2+=1
    #print(str(p1)+" "+str(p2))
    if(p1>p2):
      return 2
    else:
      return 1
  
  def last_player_move(self,state:np.array)-> int:
    """
    Find which player has the move in the provided state of the board object.

      Player "1" goes first (MAX), then "2" (MIN), etc.

      :Parameters  state:  A numpy array that represents the board
      :returns    Player whose turn it is to move
    """
    if(state.shape[0]==0):
      return 0
    return state[self.pieceOrder[-1].y][self.pieceOrder[-1].x]
  
  def actions(self,state:np.array)-> set[p.point]:
    """
    Gives the set of the possible actions that can be taken as a set of points

      Player "1" goes first (MAX), then "2" (MIN), etc.

      :Parameters  state:  A numpy array that represents the board
      :returns    Player whose turn it is to move
    """
    values:set[p.point]=set()
    for i in range(state.shape[0]):
      for j in range(state.shape[1]):
        if(state[i][j]==0):
          values.add(p.point(i,j))
    """for i in range(state.shape[0]):
      #for j in range(state.shape[1]):
        if(state[0][i]==0):
          values.add(p.point(i,0))"""
    return values
  
  def result(self,state:np.array,action:p.point)-> np.array:
    """Simulate the result of applying the given action in the provided state.

        The state contains information on which player (MAX or MIN) should move next.
            MAX is connect4 player "1", represented by a board entry of 1
            MIN is connect4 player "2", represented by a board entry of 2

        :param      state       Game state in which the action is applied represented as a numpy array
        :param      action      Action applied in the game as a point to place the piece
        :returns    Resulting state after applying the action
        """
    stateCopy=np.copy(state)
    player=self.current_player(stateCopy)
    #print("Player"+str(player))
    self.placePiece(stateCopy,action.x,player)
    return stateCopy
  
  def result_multiple(self,state:np.array,actions:list[p.point])-> np.array:
    """Simulate the result of applying multiple actions from the given state.

        :param      state       Game state from which the actions are applied
        :param      actions     List of actions
        :returns    Resulting state after applying the actions, in list order
    """
    curr_state = state
    i=0
    while(i<len(actions)):
      curr_state = self.result(curr_state, actions[i])
      i+=1
    return curr_state
  
  def who_is_winner(self,state:np.array)->int:
    """The method determines if there is a winner for the game and who it is
        0 is no player
        1 is player 1
        2 is player 2

    Parameters
    ----------
    state : np.array
      The 2d array representing the game board

    Returns
    -------
      Returns the player who won"""
    player=0
    for i in range(state.shape[0]):
      for j in range(state.shape[1]):
        player=state[i][j]
        if(player!=0 and self.checkWin(state,player,p.point(i,j))):
            return player
    return 0
  
  def is_terminal(self, state:np.array)->bool:
    """Checks if the game is over in the current state

    Parameters
    ----------
    state : np.array
      The 2d array representing the game board
    
    Returns
    -------
      Returns true or false if the game is in a finished state"""
    #if full and if winner if found
    isFull=True
    for i in range(state.shape[0]):
      for j in range(state.shape[1]):
        if(state[i][j]==0):
          isFull=False
    if(isFull):
      return True
    return self.who_is_winner(state)!=0
  def utility(self, state:np.array)-> float:
    """The method finds the value of the terminal state and works for both players perspectives

        in the game of connect 4
          1 is player 1 winning
          0 is player 2 winning
          0.5 is a draw
          
    Parameters
    ----------
    state : np.array
      The 2d array representing the game board

    Returns
    -------
      Returns a value for the utility of the state"""
    player=self.who_is_winner(state)
    match player:
      case 0:
        return 0.5
      case 1:
        return 1
      case 2:
        return 0
    
  
    

  

  


