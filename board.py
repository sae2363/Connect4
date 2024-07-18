import numpy as np
import point as p
class board:
  #stores the game board data
  array:int
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

  def placePiece(self,colum:int,player:int)-> bool:
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
    if(self.array[0][colum]):
      return False
    i=0
    while(i<self.array.shape[0] and self.array[i][colum]==0):
      i+=1
    self.array[i-1,colum]=player
    self.pieceOrder.append(p.point(i-1,colum))
    return True

  
  def checkWin(self,player:int):
    """
    The method determines if there is a winner for the game by checking the last placed piece by the player

    Parameters
    ----------
    player : int
      the number the player is.  Starts at 1 and goes up. (zero represents a empty space)

    Returns
    -------
      Returns true or false if the player indicated won
    """
    center:p.point=self.pieceOrder[-1]
    i=len(self.pieceOrder)-1
    while(self.array[center.y][center.x]!=player):
      center=self.pieceOrder[i]
      i-=1
    refPoint:p.point=p.point(center.x,center.y)
    for i in range(-1,2):
     for j in range(-1,2):
      refPoint.x=center.x+(j)
      refPoint.y=center.y+(i)
      if(refPoint.x<self.array.shape[1] and refPoint.y<self.array.shape[0] 
      and refPoint.checkVal(self.array,player)):
        if(1+self.checkWinHelper(center,j,i,player,1)+self.checkWinHelper(center,-j,-i,player,1)>=self.inARow):
          return True

    return False
  #Doc TBD just ask kyle
  def checkWinHelper(self,center:p.point,x:int,y:int,player:int,d:int)-> int:
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
    if(point2.x<self.array.shape[0] and point2.y<self.array.shape[1] and point2.x>=0 and point2.y>=0):
      #once it hits a point that is not the player then backtrack
      if(not(point2.checkVal(self.array,player))):
        return 0
      else:
        return 1+self.checkWinHelper(center,x,y,player,(d+1))
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


