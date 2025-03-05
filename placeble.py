"""
this shit was done by the legendary cam, any questions pls text me or smth idk, i tried to make it easy to understand but idk
"""
from abc import ABC, abstractmethod # abstract method
from player_colors import PlayerColors # starter file
from position import Position # starter file
from typing import List, Optional # helps is_valid_placement
from game_piece import GamePiece # for is_valid_placement

class Placeble(ABC):
    def __init__(self, color: PlayerColors): # makes sure the player color is one of the two enum options from player_colors.py
        if not isinstance(color, PlayerColors):
            raise TypeError("Color must be of type PlayerColors")
        self.__color = color

    @property
    def color(self) -> PlayerColors: # getter method
        return self.__color

    @abstractmethod
    def __str__(self) -> str: # makes sure all child classes has this method
        pass

    @abstractmethod
    def is_valid_placement(self, pos: Position, board: List[List[Optional[GamePiece]]]) -> bool:
        if not isinstance(pos, Position): # makes sure that pos is an instance of position class
            return False
        if not (0 <= pos.row < len(board) and 0 <= pos.col < len(board[0])): # makes sure the row and col values are within the valid range of the board, len(board) is number of rows, len(board[0]) is number of columns
            return False
        if board[pos.row][pos.col] is not None: # makes sure that slot doesnt already have a stone, (if the position is occupied (not none))
            return False
        return True
