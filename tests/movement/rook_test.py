from pytest import mark as m
from src.board import Board
from src.pieces import Rook
from src.utils import indexes_to_algebraic

test_board = Board().init_empty_board()
test_white_rook = Rook(row=6, column=4, is_white=True)
test_black_rook = Rook(row=2, column=4, is_white=False)


@m.describe("Test Rook Logic")
class TestRook:
    @m.context("Test rook movement vectors")
    @m.it("Rook should have its correct movement vectors")
    def test_movement_vectors_white_pawn(self):
        expected_white_pawn_movement_vectors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        assert all(
            [
                movement_vector in test_white_rook._movement_vectors
                for movement_vector in expected_white_pawn_movement_vectors
            ]
        )

    @m.context("Test rook possible moves")
    @m.it("Rook should be able to move as much as possible according to its vectors")
    def test_empty_board_rook_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        rook = Rook(row=initial_row, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(rook)
        print(test_board)
        rook.update_possible_moves(test_board.squares)
        expected_possible_moves_same_column = ["e1", "e2", "e3", "e5", "e6", "e7", "e8"]
        expected_possible_moves_same_row = ["a4", "b4", "c4", "d4", "f4", "g4", "h4"]
        expected_moves = expected_possible_moves_same_column + expected_possible_moves_same_row
        assert len(rook.possible_moves) == len(expected_moves)
        for expected_possible_move in expected_moves:
            assert expected_possible_move in rook.possible_moves

    @m.context("Test rook possible moves")
    @m.it("Rook should'n be able to move if a same color piece blocks the way")
    def test_blocking_piece_rook_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        rook_e4 = Rook(row=initial_row, column=initial_column, is_white=True)
        blocking_rook_g4 = Rook(row=initial_row, column=initial_column + 2, is_white=True)
        blocking_rook_e7 = Rook(row=initial_row - 2, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(rook_e4, blocking_rook_g4, blocking_rook_e7)
        rook_e4.update_possible_moves(test_board.squares)
        expected_possible_moves_same_column = ["e1", "e2", "e3", "e5"]
        expected_possible_moves_same_row = ["a4", "b4", "c4", "d4", "f4"]
        expected_moves = expected_possible_moves_same_column + expected_possible_moves_same_row
        assert len(rook_e4.possible_moves) == len(expected_moves)
        for expected_possible_move in expected_moves:
            assert expected_possible_move in rook_e4.possible_moves

    @m.context("Test rook possible moves")
    @m.it("Rook should be able to capture opposing pieces")
    def test_capturing_piece_rook_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        rook_e4 = Rook(row=initial_row, column=initial_column, is_white=True)
        capturable_rook_g4 = Rook(row=initial_row, column=initial_column + 2, is_white=False)
        blocking_rook_e7 = Rook(row=initial_row - 2, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(rook_e4, capturable_rook_g4, blocking_rook_e7)
        rook_e4.update_possible_moves(test_board.squares)
        expected_possible_moves_same_column = ["e1", "e2", "e3", "e5"]
        expected_possible_moves_same_row = ["a4", "b4", "c4", "d4", "f4", "g4"]
        expected_moves = expected_possible_moves_same_column + expected_possible_moves_same_row
        print(rook_e4.possible_moves)
        assert len(rook_e4.possible_moves) == len(expected_moves)
        for expected_possible_move in expected_moves:
            assert expected_possible_move in rook_e4.possible_moves
