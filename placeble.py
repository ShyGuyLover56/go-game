
# this shit was done by the legendary cam, any questions pls text me or smth idk, i tried to make it easy to understand but idk

from abc import ABC, abstractmethod # abstract method
from player_colors import PlayerColors # starter file
from position import Position # starter file


class Placeble(ABC):
    """
    Abstract base class for all placeable objects on the board.

    Ensures that all child classes define the necessary attributes and methods related to placing a game piece on the board.
    """
    def __init__(self, color: PlayerColors): # makes sure the player color is one of the two enum options from player_colors.py
        """
        Initializes the Placeble object with a specified color.

        Args:
            color (PlayerColors): The color of the piece, must be an instance of the PlayerColors enum.

        Raises:
            TypeError: If the provided color is not an instance of PlayerColors.
        """
        if not isinstance(color, PlayerColors):
            raise TypeError("Color must be of type PlayerColors")
        self.__color = color

    @property
    def color(self) -> PlayerColors: # getter method
        """
        Gets the color of the placeable object.

        Returns:
            PlayerColors: The color of the object.
        """
        return self.__color

    @abstractmethod
    def __str__(self) -> str: # makes sure all child classes has this method
        """
        Returns a string representation of the placeable object.

        Returns:
            str: A string that represents the object.
        """
        pass

    @abstractmethod
    def is_valid_placement(self, pos: Position, board) -> bool:
        """
        Checks if the placement of the object is valid at the given position on the board.

        Args:
            pos (Position): The position to check for validity.
            board (list[list[Optional[Placeble]]]): The game board represented as a 2D list where each element is either None or a placeable object.

        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        if not isinstance(pos, Position): # makes sure that pos is an instance of position class
            return False
        if not (0 <= pos.row < len(board) and 0 <= pos.col < len(board[0])): # makes sure the row and col values are within the valid range of the board, len(board) is number of rows, len(board[0]) is number of columns
            return False
        if board[pos.row][pos.col] is not None: # makes sure that slot doesnt already have a stone, (if the position is occupied (not none))
            return False
        return True
