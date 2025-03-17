from http.cookiejar import liberal_is_HDN
from typing import List, Optional
from position import Position
from player_colors import PlayerColors
from game_piece import GamePiece
from game_player import GamePlayer

class GoModel():
    def __init__(self, rows: int = 6, cols: int = 6):
        if rows not in [6, 9, 11, 13, 19] or cols not in [6, 9, 11, 13, 19]:
            raise ValueError("Invalid board size: board size must be 6x6, 9x9, 11x11, 13x13, or 19x19")

        self.__nrows = rows #number of rows on the board
        self.__ncols = cols #number of columns on the board
        self.__board: List[List[Optional[GamePiece]]] = [[None for i in range(cols)] for j in range(rows)] #initializes the board
        self.__current_player = GamePlayer(PlayerColors.BLACK) #Black starts first, per Go rules
        self.__message = "" #message to be displayed to the players
        self.__history = [] #Stores board save-states for undo function

    @property
    def nrows(self) -> int:
        return self.__nrows

    @property
    def ncols(self) -> int:
        return self.__ncols

    @property
    def board(self) -> List[List[Optional[GamePiece]]]:
        return self.__board

    @property
    def current_player(self) -> GamePlayer:
        return self.__current_player

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, msg: str):
        self.__message = msg

    def piece_at(self, pos: Position) -> Optional[GamePiece]:
        if self.__nrows > pos.row >= 0 and self.__ncols > pos.col >= 0:
            return self.__board[pos.row][pos.col]
        raise ValueError("Out of bounds!")

    def set_piece(self, pos: Position, piece: Optional[GamePiece] = None):
        pass

    def set_next_player(self):
        if self.__current_player.player_color == PlayerColors.BLACK:
            self.__current_player = GamePlayer(PlayerColors.WHITE)
        else:
            self.__current_player = GamePlayer(PlayerColors.BLACK)

    def pass_turn(self):
        self.__current_player.skip_count += 1
        if self.__current_player.skip_count >=2:
            self.__message = "Game Over: Two consecutive passes were made"

    def is_game_over(self) -> bool:
        return self.__current_player.skip_count >= 2

    def is_valid_placement(self, pos: Position, piece: GamePiece) -> bool:
        if not (self.__nrows > pos.row >= 0) and (self.__ncols > pos.col >= 0):
            return False #out of bounds
        if self.__board[pos.row][pos.col] is not None:
            return False #preoccupied position
        else:
            return True

    def capture(self):
        def capture_helper(pos, color, visited): #Finds all connected stones of the same color from the given position
            stack = [pos]
            group = set()
            liberties = set()
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                group.add(current)
                for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_pos = Position(current.row + r, current.col + c)
                    if self.__nrows > new_pos.row >= 0 and self.__ncols > new_pos.col >= 0:
                        neighbor = self.piece_at(new_pos)
                        if neighbor is None:
                            liberties.add(new_pos) #Empty space adjacent to group
                        elif neighbor.color == color:
                            stack.append(new_pos) #Continue expanding the group
            return group, liberties

        visited = set()
        to_remove = set()
        for r in range(self.__nrows):
            for c in range(self.__ncols):
                pos = Position(r, c)
                piece = self.piece_at(pos)
                if piece and pos not in visited:
                    group, liberties = capture_helper(pos, piece.color, visited)
                    if not liberties: #No liberties means the group was captured
                        to_remove.update(group)

        for pos in to_remove:
            self.__board[pos.row][pos.col] = None #Removes captured stones

    def calculate_score(self) -> List[int]: #calculates the scores for both players
        black_score = sum(row.count(GamePiece(PlayerColors.BLACK)) for row in self.__board)
        white_score = sum(row.count(GamePiece(PlayerColors.WHITE)) for row in self.__board)

        black_captures = 0
        white_captures = 0

        white_score += 6.5 #Komi bonus

        return [black_score + black_captures, white_score + white_captures]

    def undo(self):
        if not self.__history:
            raise UndoException("Nothing to undo")
        self.__board = self.__history.pop()

class UndoException(Exception):
    pass