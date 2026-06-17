import sys
import os
import chess
import unittest

# Allow importing from src/ without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from material import calculate_material, PIECE_VALUES


class TestCalculateMaterial(unittest.TestCase):

    def test_starting_position_is_equal(self):
        """Both sides start with the same material total."""
        board = chess.Board()
        white, black = calculate_material(board)
        self.assertEqual(white, black)

    def test_starting_position_value(self):
        """Starting material = 8*1 + 2*3 + 2*3 + 2*5 + 1*9 = 39 per side."""
        board = chess.Board()
        white, black = calculate_material(board)
        self.assertEqual(white, 39)
        self.assertEqual(black, 39)

    def test_empty_board_returns_zero(self):
        """An empty board has no material for either side."""
        board = chess.Board(fen=None)  # creates truly empty board
        white, black = calculate_material(board)
        self.assertEqual(white, 0)
        self.assertEqual(black, 0)

    def test_white_captures_black_queen(self):
        """After removing black's queen, black material drops by 9."""
        board = chess.Board()
        # Remove black queen from d8
        board.remove_piece_at(chess.D8)
        white, black = calculate_material(board)
        self.assertEqual(white, 39)
        self.assertEqual(black, 30)

    def test_black_captures_white_rook(self):
        """After removing a white rook, white material drops by 5."""
        board = chess.Board()
        board.remove_piece_at(chess.A1)
        white, black = calculate_material(board)
        self.assertEqual(white, 34)
        self.assertEqual(black, 39)

    def test_king_has_no_material_value(self):
        """Kings are not counted in material (value = 0)."""
        # Board with only kings
        board = chess.Board(fen=None)
        board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
        white, black = calculate_material(board)
        self.assertEqual(white, 0)
        self.assertEqual(black, 0)

    def test_single_piece_values(self):
        """Each piece type scores its correct value in isolation."""
        piece_map = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }
        for piece_type, expected_value in piece_map.items():
            board = chess.Board(fen=None)
            board.set_piece_at(chess.E4, chess.Piece(piece_type, chess.WHITE))
            white, black = calculate_material(board)
            self.assertEqual(white, expected_value, msg=f"Failed for piece type {piece_type}")
            self.assertEqual(black, 0, msg=f"Black should be 0 for piece type {piece_type}")

    def test_returns_tuple_of_two_integers(self):
        """Return type must be a 2-tuple of integers."""
        board = chess.Board()
        result = calculate_material(board)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], int)


if __name__ == "__main__":
    unittest.main()
