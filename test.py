import unittest
from player_colors import PlayerColors
from position import Position
from placeble import Placeble


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


if __name__ == '__main__':
    unittest.main()
