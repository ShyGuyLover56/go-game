
# more work done by cam

from placeble import Placeble
from player_colors import PlayerColors
from position import Position

class GamePiece(Placeble):
    """
        A class representing a game piece in the game, inheriting from Placeble.

        The GamePiece represents a piece that can be placed on the game board, and has methods to determine valid placement and equality comparison.
        """
    def __str__(self) -> str:
        """
        Returns a string representation of the GamePiece.

        Returns:
            str: A string that represents the GamePiece, showing its color.
        """
        return f'GamePiece({self.color.name})' # GamePiece(BLACK) or GamePiece(WHITE)

    def is_valid_placement(self, pos: Position, board) -> bool:
        """
        Checks if placing the game piece at the specified position is valid.

        This method first checks basic placement validity using the parent class method, then checks for the surrounding environment to ensure the piece is not fully surrounded by opponent pieces.

        Args:
            pos (Position): The position to check for validity.
            board (list[list[Optional[Placeble]]]): The game board represented as a 2D list where each element is either None or a placeable object.

        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        if not super().is_valid_placement(pos, board): # if the placement on the board is not valid from placeble.py
            return False

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # defines left, right, down, up
        opponent_color = self.color.opponent() # the color of the opposing player

        has_liberty = False # checks if the piece has an empty space or friendly piece nearby
        is_surrounded = True # might use for calculate score but currently isn't being used

        for dr, dc in directions: # checks the spot on each side
            new_row, new_col = pos.row + dr, pos.col + dc # pos.row and pos.col represent the current row and column where the piece is being placed, dr and dc come from directions, which is a list of row and column adjustments for checking adjacent positions
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]): # makes sure new_row and new_col are inside the board and not out of range
                neighbor = board[new_row][new_col] # if the position (new_row, new_col) is valid (inside the board(previous line)) we can check what’s there
                if neighbor is None: # there is an open space on one of the sides
                    has_liberty = True
                elif neighbor.color == self.color: # that neighbor happens to be your own piece
                    has_liberty = True
                elif neighbor.color == opponent_color: # ignore if it's an opponent piece
                    continue
        return has_liberty # true = piece isn't surrounded, false = piece is surrounded

    def __eq__(self, other) -> bool: # REDIFINING THE QUEALS SO PRAIRIE LEARN WORKS
        """
        Compares this GamePiece with another GamePiece for equality.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if both GamePieces have the same color, False otherwise.
        """
        if not isinstance(other, GamePiece):
            return False
        return self.color == other.color

    def equals(self, other) -> bool:
        """
        Checks if this GamePiece is equal to another GamePiece.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if both GamePieces are equal, False otherwise.
        """
        return self == other

    """def equals(self, other) -> bool: # my old equals if you care
        if not isinstance(other, GamePiece): # if other is not a GamePiece then false
            return False
        return self.color == other.color # if both pieces are the same color return true, else return false"""
