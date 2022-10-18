from pytest import mark as m
from src.board import Board
from src.pieces import King

test_board = Board().init_empty_board()
test_white_king = King(row=6, column=4, is_white=True)
test_black_king = King(row=2, column=4, is_white=False)


@m.describe("Test King Logic")
class TestKingk:
    @m.context("Test king movement vectors")
    @m.it("King should have its correct movement vectors")
    def test_movement_vectors_white_king(self):
        expected_white_king_movement_vectors = [(-1, -1), (-1, 1), (-1, 0), (1, -1), (1, 1), (1, 0), (0, -1), (0, 1)]
        assert all(
            [
                movement_vector in test_white_king._movement_vectors
                for movement_vector in expected_white_king_movement_vectors
            ]
        )

    @m.context("Test king possible moves")
    @m.it("King should be able to move as much as possible according to its vectors")
    def test_empty_board_king_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        king = King(row=initial_row, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(king)
        king.update_possible_moves(test_board.squares)
        expected_possible_moves = ["d4", "f4", "e5", "e3", "d5", "f5", "d3", "f3"]
        assert len(king.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in king.possible_moves

    @m.context("Test king possible moves")
    @m.it("King shouldn't be able to move where a piece of the same color is")
    def test_blocking_white_piece_king_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        king = King(row=initial_row, column=initial_column, is_white=True)
        blocking_king_d5 = King(row=initial_row - 1, column=initial_column - 1, is_white=True)
        blocking_king_f3 = King(row=initial_row + 1, column=initial_column + 1, is_white=True)
        test_board.init_board_with_pieces(king, blocking_king_d5, blocking_king_f3)
        king.update_possible_moves(test_board.squares)
        expected_possible_moves = ["d4", "f4", "e5", "e3", "f5", "d3"]
        assert len(king.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in king.possible_moves

    @m.context("Test king possible moves")
    @m.it("King should be able to move where a piece of the opposite color is")
    def test_capturing_white_piece_king_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        king = King(row=initial_row, column=initial_column, is_white=True)
        blocking_king_d5 = King(row=initial_row - 1, column=initial_column - 1, is_white=True)
        opposing_king_f3 = King(row=initial_row + 1, column=initial_column + 1, is_white=False)
        test_board.init_board_with_pieces(king, blocking_king_d5, opposing_king_f3)
        king.update_possible_moves(test_board.squares)
        print(test_board)
        print(king.possible_moves)
        expected_possible_moves = ["d4", "f4", "e5", "e3", "f5", "d3", "f3"]
        assert len(king.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in king.possible_moves
