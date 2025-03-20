from typing import List, Optional
from position import Position
from player_colors import PlayerColors
from game_piece import GamePiece
from game_player import GamePlayer

class GoModel: # starting over

    valid_sizes = {6, 9, 11, 13, 19}

    def __init__(self, rows: int = 6, cols: int = 6):

        if rows not in self.valid_sizes or cols not in self.valid_sizes:
            raise ValueError("board size must be a valid size")

        # boars stuff
        self.__nrows = rows
        self.__ncols = cols
        self.__board: List[List[Optional[GamePiece]]] = [[None for _ in range(cols)] for _ in range(rows)]
        # self.__current_player = GamePlayer(PlayerColors.BLACK)
        self.__message = ""

        # player stuff
        self.__black_player = GamePlayer(PlayerColors.BLACK)
        self.__white_player = GamePlayer(PlayerColors.WHITE)
        self.__current_player = self.__black_player # black goes first

        # move history for undo
        self.__move_history = [] # stores previous game states for undo
        self.__previous_board_states = [] # tracks past boards for ko role

        #

    @property # readable
    def nrows(self) -> int:
        return self.__nrows # number of rows

    @property # readable
    def ncols(self) -> int:
        return self.__ncols # number of columns

    @property # readable
    def current_player(self) -> GamePlayer:
        return self.__current_player # current player, obviously

    @property # readable
    def board(self) -> List[List[Optional[GamePiece]]]:
        return self.__board # current board state

    @property # readable
    def message(self) -> str:
        return self.__message # current game message

    @message.setter # writable
    def message(self, msg: str):
        if not isinstance(msg, str):
            raise TypeError("message must be a string")
        self.__message = msg # sets a new message

    def piece_at(self, pos: Position) -> Optional[GamePiece]:
        if not (0 <= pos.row < self.__nrows and 0 <= pos.col < self.__ncols):
            raise ValueError("out of bounds")
        return self.__board[pos.row][pos.col] # return a game piece at a given position

    def set_piece(self, pos: Position, piece: Optional[GamePiece]) -> None:
        """if not (0 <= pos.row < self.__nrows and 0 <= pos.col < self.__ncols):
            raise ValueError("out of bounds")"""
        if not self.is_valid_placement(pos, piece):
            return

        # saves current board state
        self.__move_history.append({
            "board": [row[:] for row in self.__board],
            "player": self.__current_player,
            "captures": {p.player_color: p.capture_count for p in [self.__black_player, self.__white_player]},
            "skips": {p.player_color: p.skip_count for p in [self.__black_player, self.__white_player]}
            })

        self.__board[pos.row][pos.col] = piece # places a game piece at a given position
        self.__previous_board_states.append(row[:] for row in self.__board)
        self.set_next_player()

    def set_next_player(self) -> None:
        next_color = self.__current_player.player_color.opponent() # opponent comes from player_colors.py file
        self.__current_player = GamePlayer(next_color) # switches turn to next player

    def pass_turn(self) -> None:
        self.__current_player.skip_count += 1

        if self.__current_player.skip_count >= 2: # if both players pass the game ends
            self.__message = "game over"

        self.set_next_player() # switches turn to next player

    def is_game_over(self) -> bool:
        return self.__current_player.skip_count >= 2 # returns as true if both players passed, aka game over

    def is_valid_placement(self, pos: Position, piece: GamePiece) -> bool: # checks if given position is valid before placing the actual piece
        if not (0 <= pos.row < self.__nrows and 0 <= pos.col < self.__ncols): # checks out of bounds
            self.__message = "out of bounds"
            return False

        if self.__board[pos.row][pos.col] is not None: # if that position is already taken
            self.__message = "position already taken"
            return False

        if not piece.is_valid_placement(pos, self.__board): # is_valid_placement from game_piece.py
            self.__message = "no liberties (is_valid_placement failed)"
            return False

        if self.__check_ko_rule(pos, piece): # ko rule is loop of being captured over and over again
            self.__message = "ko rule violated"
            return False

        return True

    def __check_ko_rule(self, pos: Position, piece: GamePiece) -> bool: # used with is_valid_placement, ko rile is loop of being captured over and over again
        simulated_board = [row[:] for row in self.__board]  # copy board state
        simulated_board[pos.row][pos.col] = piece  # place the piece

        return simulated_board in self.__previous_board_states  # compare past states

    def __has_liberty(self, pos: Position, visited: set) -> bool: # capture helper method, a set is a unorganized collection of elements that is mutable
        if pos in visited:
            return False  # already checked position
        visited.add(pos)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up down left right

        for dr, dc in directions: # moves to each of the 4 neighboring positions
            new_row, new_col = pos.row + dr, pos.col + dc

            if 0 <= new_row < self.__nrows and 0 <= new_col < self.__ncols: # checks if new position is within board boundaries
                neighbor = self.__board[new_row][new_col]
                if neighbor is None:  # found a liberty
                    return True
                if neighbor.color == self.__board[pos.row][pos.col].color: # if the neighbor color is the same color
                    if self.__has_liberty(Position(new_row, new_col), visited): # recursively check that stone
                        return True

        return False # if all adjacent positions have been checked and no liberties are found return false

    def capture(self) -> None:

        opponent_color = self.__current_player.player_color.opponent() # gets opponent color
        captured_positions = [] # list for captures positions (stones with no liberties)

        # finds all pieces that are surrounded
        for row in range(self.__nrows):
            for col in range(self.__ncols): # loops through every position on the board
                piece = self.__board[row][col]
                if piece and piece.color == opponent_color:# if a piece is found and is opponent color it will be checked for liberties
                    if not self.__has_liberty(Position(row, col), set()): # calls __has_liberty to check if the opponents piece has at least 1 empty adjacent space, if no liberties are found false is returned and the position is added to captured_positions
                        captured_positions.append(Position(row, col))

        # remove captured stones and update capture count
        for pos in captured_positions: # iterates through all captured positions
            self.__board[pos.row][pos.col] = None # removes them from the board by setting their position to none
            self.__current_player.capture_count += 1 # capture count goes up for current player

        # update game message
        if captured_positions:
            self.__message = f"{self.__current_player.player_color.name} captured {len(captured_positions)} pieces"
        else:
            self.__message = f"no captures this turn"

    def calculate_score(self) -> dict:
        # sets each score equal to their capture count
        black_score = self.__black_player.capture_count
        white_score = self.__white_player.capture_count

        visited = set()  # set that keeps track of empty spaces that have already been checked to prevent doubles

        # iterate over every position on the board
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                if self.__board[row][col] is None and (row, col) not in visited: # if an empty is found and hasnt been checked before, it could belong to a territory

                    territory_positions = set()
                    surrounding_colors = set()

                    self.__flood_fill_territory(Position(row, col), territory_positions, surrounding_colors, visited) # finds all connected empty spaces forming a potential territory, identifies which player surrounded the territory

                    # assigns points if the territory is enclosed by only one color
                    if len(surrounding_colors) == 1: # if the empty area is surrounded by only one player
                        owner = next(iter(surrounding_colors))  # get the single color that surrounds this area
                        if owner == PlayerColors.BLACK: # adds to respective score
                            black_score += len(territory_positions)
                        else:
                            white_score += len(territory_positions)

        # returns final score as a dictionary
        return {
            "BLACK": black_score,
            "WHITE": white_score
        }

    def __flood_fill_territory(self, pos: Position, territory_positions: set, surrounding_colors: set, visited: set) -> None: # helper method for calculate score

        if (pos.row, pos.col) in visited: # already checked the position
            return  # prevents infinite loops

        visited.add((pos.row, pos.col))  # mark starting position visited
        queue = [pos]  # list of empty positions on the board being explored as part of a territory

        while queue:
            current = queue.pop(0) # removes position from queue...
            territory_positions.add((current.row, current.col))  # and adds it to the territory

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up down left right
            for dr, dc in directions:
                new_row, new_col = current.row + dr, current.col + dc
                if 0 <= new_row < self.__nrows and 0 <= new_col < self.__ncols: # out of bounds

                    neighbor = self.__board[new_row][new_col]

                    if neighbor is None:  # if neighbor is empty space
                        if (new_row, new_col) not in visited: # if neighbor is empty, add it to territory
                            queue.append(Position(new_row, new_col)) # add it to queue
                            visited.add((new_row, new_col))
                    else:
                        surrounding_colors.add(neighbor.color)  # add surrounding stone color

    def undo(self):
        if not self.__move_history: # if there is nothing in the move history we cant undo
            raise UndoException("nothing in move history")

        # undoes the game
        last_state = self.__move_history.pop()
        self.__board = last_state["board"]
        self.__current_player = last_state["player"]
        self.__message = "undo"

        # capture and skip count for when i do it
        self.__current_player.capture_count = last_state["captures"][self.__current_player.player_color]
        self.__current_player.skip_count = last_state["skips"][self.__current_player.player_color]

        if self.__previous_board_states: # prevents 2 of the same board in previous_board_states list
            self.__previous_board_states.pop()

class UndoException(Exception):
    pass

