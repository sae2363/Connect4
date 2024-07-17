import numpy as np
class board:
  array:int
  inARow:int
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
    array = np.zeros((size, size))
    inARow=inARowToWin

  def placePiece(colum:int,player:int):
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
    none
    """
  #Todo make/decide the function
  def checkWin():
    return False

