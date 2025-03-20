import unittest
from player_colors import PlayerColors
from position import Position
from placeble import Placeble
from game_piece import GamePiece
from game_player import GamePlayer

class TestPlaceble(unittest.TestCase): # all of this done by cam

    def test_init_valid_color(self):
        valid_color = PlayerColors.BLACK
        piece = Placeble(valid_color)
        self.assertEqual(piece.color, valid_color)

    def test_init_invalid_color(self):
        invalid_color = "andrew"
        with self.assertRaises(TypeError):
            Placeble(invalid_color)

    def test_is_valid_placement_valid(self):
        valid_pos = Position(1, 1)
        board = [[None, None], [None, None]]  # empty 2x2 board

        valid_color = PlayerColors.BLACK
        piece = Placeble(valid_color)
        result = piece.is_valid_placement(valid_pos, board)
        self.assertTrue(result, "valid placement")

    def test_is_valid_placement_out_of_bounds(self):
        invalid_pos = Position(5, 5)  # position outside 2x2
        board = [[None, None], [None, None]]  # another empty 2x2 board
        valid_color = PlayerColors.BLACK
        piece = Placeble(valid_color)

        result = piece.is_valid_placement(invalid_pos, board)
        self.assertFalse(result, "out. of. motherfucking. bounds.")

    def test_is_valid_placement_occupied(self):
        occupied_pos = Position(0, 0)
        board = [[Placeble(PlayerColors.BLACK), None], [None, None]]  # 0,0 is a black piece in a 2x2 board

        valid_color = PlayerColors.WHITE
        piece = Placeble(valid_color)

        result = piece.is_valid_placement(occupied_pos, board)
        self.assertFalse(result, "it would be cool if the pieces could physically stack vertically but its unfortunately not the case")

    def test_is_valid_placement_invalid_position(self):
        invalid_pos = "invalid position"  # not an instance of Position
        board = [[None, None], [None, None]]  # empty 2x2 board
        valid_color = PlayerColors.WHITE
        piece = Placeble(valid_color)

        result = piece.is_valid_placement(invalid_pos, board)
        self.assertFalse(result, "invalid placement")

    def test_is_valid_placement_with_friendly_piece(self):
        friendly_pos = Position(0, 1)
        board = [[None, Placeble(PlayerColors.BLACK)], [None, None]]  # 0,1 is a friendly piece

        valid_color = PlayerColors.BLACK
        piece = Placeble(valid_color)

        result = piece.is_valid_placement(friendly_pos, board)
        self.assertTrue(result, "valid placement because of friendly piece")

class TestGamePiece(unittest.TestCase): # meow, get it, meow, like the beanie i wear every day

    def test_gamepiece_init(self):
        piece = GamePiece(PlayerColors.BLACK) # proper initialization
        self.assertEqual(piece.color, PlayerColors.BLACK)

    def test_gamepiece_str(self):
        piece = GamePiece(PlayerColors.WHITE) # proper string
        self.assertEqual(str(piece), "GamePiece(WHITE)")

    def test_is_valid_placement_valid(self):
        board = [[None for _ in range(5)] for _ in range(5)]  # empty 5x5 board
        piece = GamePiece(PlayerColors.BLACK)
        pos = Position(2, 2)
        self.assertTrue(piece.is_valid_placement(pos, board)) # place game piece is empty valid position

    def test_is_valid_placement_invalid_out_of_bounds(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        piece = GamePiece(PlayerColors.BLACK)
        pos = Position(6, 6)  # out of bounds
        self.assertFalse(piece.is_valid_placement(pos, board))

    def test_is_valid_placement_invalid_occupied(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        piece1 = GamePiece(PlayerColors.BLACK)
        piece2 = GamePiece(PlayerColors.WHITE)
        board[2][2] = piece1  # position already occupied
        pos = Position(2, 2)
        self.assertFalse(piece2.is_valid_placement(pos, board)) # checking already occupied position

    def test_is_valid_placement_surrounded(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        piece = GamePiece(PlayerColors.BLACK)
        pos = Position(2, 2) # middle of the diamond

        # surrounding opponent pieces
        board[1][2] = GamePiece(PlayerColors.WHITE)
        board[3][2] = GamePiece(PlayerColors.WHITE)
        board[2][1] = GamePiece(PlayerColors.WHITE)
        board[2][3] = GamePiece(PlayerColors.WHITE)

        self.assertFalse(piece.is_valid_placement(pos, board))

    def test_gamepiece_equality(self):
        piece1 = GamePiece(PlayerColors.BLACK)
        piece2 = GamePiece(PlayerColors.BLACK)
        self.assertEqual(piece1, piece2) # they should be on the same team

    def test_gamepiece_inequality(self):
        piece1 = GamePiece(PlayerColors.BLACK)
        piece2 = GamePiece(PlayerColors.WHITE)
        self.assertNotEqual(piece1, piece2) # they should not be on the same team

    def test_equals_method(self):
        piece1 = GamePiece(PlayerColors.BLACK)
        piece2 = GamePiece(PlayerColors.BLACK)
        self.assertTrue(piece1.equals(piece2)) # they should be equals

    def test_equals_method_false(self):
        piece1 = GamePiece(PlayerColors.BLACK)
        piece2 = GamePiece(PlayerColors.WHITE)
        self.assertFalse(piece1.equals(piece2)) # they should not be equals

class TestGamePlayer(unittest.TestCase): # brr skibidi dob dob dob yes yes

    def test_game_player_init(self): # proper initialization
        player = GamePlayer(PlayerColors.BLACK)
        self.assertEqual(player.player_color, PlayerColors.BLACK)
        self.assertEqual(player.capture_count, 0)
        self.assertEqual(player.skip_count, 0)

    def test_game_player_init_invalid_color(self):
        with self.assertRaises(TypeError):
            GamePlayer("blues")  # blues, like the angry bird that can split into three

    def test_game_player_init_negative_captures(self):
        with self.assertRaises(ValueError):
            GamePlayer(PlayerColors.BLACK, capture_count=-1) # negative capture count

    def test_game_player_init_negative_skips(self):
        with self.assertRaises(ValueError):
            GamePlayer(PlayerColors.BLACK, skip_count=-1) # negative skip count

    def test_capture_count_setter_valid(self):
        player = GamePlayer(PlayerColors.WHITE)
        player.capture_count = 5 # updating capture count
        self.assertEqual(player.capture_count, 5)

    def test_capture_count_setter_invalid(self):
        player = GamePlayer(PlayerColors.WHITE)
        with self.assertRaises(ValueError):
            player.capture_count = -3 # negative capture count

    def test_skip_count_setter_valid(self):
        player = GamePlayer(PlayerColors.BLACK)
        player.skip_count = 2 # updating skip count
        self.assertEqual(player.skip_count, 2)

    def test_skip_count_setter_invalid(self):
        player = GamePlayer(PlayerColors.BLACK)
        with self.assertRaises(ValueError): # negative skip count
            player.skip_count = -1

    def test_game_player_str(self):
        player = GamePlayer(PlayerColors.WHITE, capture_count=3, skip_count=1)
        self.assertEqual(str(player), "GamePlayer(color: WHITE, captures: 3, skips: 1)") # printing has proper formatting

if __name__ == '__main__':
    unittest.main()
