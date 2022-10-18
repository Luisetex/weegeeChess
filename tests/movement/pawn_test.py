from pytest import mark as m
from src.board import Board
from src.pieces import Pawn
from src.utils import indexes_to_algebraic

test_board = Board()
test_white_pawn = Pawn(row=6, column=4, is_white=True)
test_black_pawn = Pawn(row=2, column=4, is_white=False)


@m.describe("Test Pawn Logic")
class TestPawn:
    @m.context("Test pawn movement vectors")
    @m.it("White pawn should have its correct movement vectors")
    def test_movement_vectors_white_pawn(self):
        expected_white_pawn_movement_vectors = [(-1, 0)]
        assert all(
            [
                movement_vector in test_white_pawn._movement_vectors
                for movement_vector in expected_white_pawn_movement_vectors
            ]
        )

    @m.context("Test pawn movement vectors")
    @m.it("White pawn should have its correct capture vectors")
    def test_capture_vectors_white_pawn(self):
        expected_white_pawn_capture_vectors = [(1, 1), (1, -1)]
        assert all(
            [
                movement_vector in test_white_pawn._capture_vectors
                for movement_vector in expected_white_pawn_capture_vectors
            ]
        )

    @m.context("Test pawn movement vectors")
    @m.it("White pawn should be able to move two squares only in its initial row")
    def test_initial_moves_white_pawn(self):
        test_board = Board()
        initial_row = 6  # 2 in algebraic
        # Pawn at e2
        for column in range(8):
            white_pawn = Pawn(row=initial_row, column=column, is_white=True)
            test_board.squares[initial_row][column] = white_pawn
            white_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(initial_row - 1, column) in white_pawn.possible_moves
            assert indexes_to_algebraic(initial_row - 2, column) in white_pawn.possible_moves
        test_board = Board()
        next_row = initial_row - 1
        for column in range(8):
            white_pawn = Pawn(row=next_row, column=column, is_white=True)
            test_board.squares[next_row][column] = white_pawn
            white_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(next_row - 1, column) in white_pawn.possible_moves
            assert indexes_to_algebraic(next_row - 2, column) not in white_pawn.possible_moves

    @m.context("Test pawn movement vectors")
    @m.it("If next square is blocked, pawn shouldn't be able to move")
    def test_blocked_square_pawn(self):
        test_board = Board()
        initial_row = 6
        initial_column = 4
        white_pawn = Pawn(initial_row, initial_column, True)
        blocking_white_pawn = Pawn(initial_row - 1, initial_column, True)
        test_board.init_board_with_pieces(white_pawn, blocking_white_pawn)
        white_pawn.update_possible_moves(test_board.squares)
        assert indexes_to_algebraic(initial_row - 1, initial_column) not in white_pawn.possible_moves
        assert indexes_to_algebraic(initial_row - 2, initial_column) not in white_pawn.possible_moves

    @m.context("Test pawn movement vectors")
    @m.it("Black pawn should have its correct movement vectors")
    def test_movement_vectors_black_pawn(self):
        expected_black_pawn_movement_vectors = [(1, 0)]
        assert all(
            [
                movement_vector in test_black_pawn._movement_vectors
                for movement_vector in expected_black_pawn_movement_vectors
            ]
        )

    @m.context("Test pawn movement vectors")
    @m.it("Black pawn should have its correct capture vectors")
    def test_capture_vectors_black_pawn(self):
        expected_black_pawn_capture_vectors = [(-1, 1), (-1, -1)]
        assert all(
            [
                movement_vector in test_black_pawn._capture_vectors
                for movement_vector in expected_black_pawn_capture_vectors
            ]
        )

    @m.context("Test pawn movement vectors")
    @m.it("Black pawn should be able to move two squares only in its initial row")
    def test_initial_moves_black_pawn(self):
        test_board = Board()
        initial_row = 1  # 7 in algebraic
        # Pawn at e7
        for column in range(8):
            black_pawn = Pawn(row=initial_row, column=column, is_white=False)
            test_board.squares[initial_row][column] = black_pawn
            black_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(initial_row + 1, column) in black_pawn.possible_moves
            assert indexes_to_algebraic(initial_row + 2, column) in black_pawn.possible_moves
        test_board = Board()
        next_row = initial_row + 1
        for column in range(8):
            black_pawn = Pawn(row=next_row, column=column, is_white=False)
            test_board.squares[next_row][column] = black_pawn
            black_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(next_row + 1, column) in black_pawn.possible_moves
            assert indexes_to_algebraic(next_row + 2, column) not in black_pawn.possible_moves
