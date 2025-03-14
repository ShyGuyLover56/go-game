"""
more work done by cam
"""
from placeble import Placeble
from player_colors import PlayerColors
from position import Position
from typing import List

class GamePiece(Placeble):
    def __str__(self) -> str:
        return f'GamePiece({self.color.name})' # GamePiece(BLACK) or GamePiece(WHITE)

    def is_valid_placement(self, pos: Position, board) -> bool:
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

    def equals(self, other) -> bool:
        if not isinstance(other, GamePiece): # if other is not a GamePiece then false
            return False
        return self.color == other.color # if both pieces are the same color return true, else return false
