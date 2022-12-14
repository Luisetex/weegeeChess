from pytest import mark as m
from src.board import Board
from src.pieces import Pawn
from src.utils import indexes_to_algebraic

test_white_pawn = Pawn(row=6, column=4, is_white=True)
test_black_pawn = Pawn(row=2, column=4, is_white=False)


@m.describe("Test Pawn Logic")
class TestPawn:
    @m.context("Test white pawn movement vectors")
    @m.it("White pawn should have its correct movement vectors")
    def test_movement_vectors_white_pawn(self):
        expected_white_pawn_movement_vectors = [(-1, 0)]
        assert all(
            [
                movement_vector in test_white_pawn._movement_vectors
                for movement_vector in expected_white_pawn_movement_vectors
            ]
        )

    @m.context("Test white pawn movement vectors")
    @m.it("White pawn should have its correct capture vectors")
    def test_capture_vectors_white_pawn(self):
        expected_white_pawn_capture_vectors = [(-1, 1), (-1, -1)]
        assert all(
            [
                movement_vector in test_white_pawn._capture_vectors
                for movement_vector in expected_white_pawn_capture_vectors
            ]
        )

    @m.context("Test white pawn possible moves")
    @m.it("White pawn should be able to move two squares only in its initial row")
    def test_initial_moves_white_pawn(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6  # 2 in algebraic
        # Pawn at e2
        for column in range(8):
            white_pawn = Pawn(row=initial_row, column=column, is_white=True)
            test_board.squares[initial_row][column] = white_pawn
            white_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(initial_row - 1, column) in white_pawn.possible_moves
            assert indexes_to_algebraic(initial_row - 2, column) in white_pawn.possible_moves
        test_board = Board()
        test_board.init_empty_board()
        next_row = initial_row - 1
        for column in range(8):
            white_pawn = Pawn(row=next_row, column=column, is_white=True)
            test_board.squares[next_row][column] = white_pawn
            white_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(next_row - 1, column) in white_pawn.possible_moves
            assert indexes_to_algebraic(next_row - 2, column) not in white_pawn.possible_moves

    @m.context("Test white pawn possible moves")
    @m.it("If next square is blocked by a white piece, pawn shouldn't be able to move")
    def test_blocked_square_by_white_piece_white_pawn(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6
        initial_column = 4
        white_pawn = Pawn(initial_row, initial_column, True)
        blocking_white_pawn = Pawn(initial_row - 1, initial_column, True)
        test_board.init_board_with_pieces(white_pawn, blocking_white_pawn)
        white_pawn.update_possible_moves(test_board.squares)
        assert indexes_to_algebraic(initial_row - 1, initial_column) not in white_pawn.possible_moves
        assert indexes_to_algebraic(initial_row - 2, initial_column) not in white_pawn.possible_moves

    @m.context("Test white pawn possible moves")
    @m.it("If next square is blocked by a black piece, pawn shouldn't be able to capture it")
    def test_blocked_square_by_black_piece_white_pawn(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6
        initial_column = 4
        white_pawn = Pawn(initial_row, initial_column, True)
        blocking_black_pawn = Pawn(initial_row - 1, initial_column, False)
        test_board.init_board_with_pieces(white_pawn, blocking_black_pawn)
        white_pawn.update_possible_moves(test_board.squares)
        assert indexes_to_algebraic(initial_row - 1, initial_column) not in white_pawn.possible_moves
        assert indexes_to_algebraic(initial_row - 2, initial_column) not in white_pawn.possible_moves

    @m.context("Test white pawn capture moves")
    @m.it("If next square is blocked by a black piece, pawn shouldn't be able to capture it")
    def test_white_pawn_capturing_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6
        initial_column = 4
        white_pawn = Pawn(initial_row, initial_column, True)
        black_pawn_a = Pawn(initial_row - 1, initial_column, False)
        black_pawn_b = Pawn(initial_row - 1, initial_column - 1, False)
        black_pawn_c = Pawn(initial_row - 1, initial_column + 1, False)
        test_board.init_board_with_pieces(white_pawn, black_pawn_a, black_pawn_b, black_pawn_c)
        white_pawn.update_possible_moves(test_board.squares)
        print(test_board)
        assert white_pawn.capture_moves
        assert indexes_to_algebraic(initial_row - 1, initial_column) not in white_pawn.capture_moves
        assert indexes_to_algebraic(initial_row - 1, initial_column - 1) in white_pawn.capture_moves
        assert indexes_to_algebraic(initial_row - 1, initial_column + 1) in white_pawn.capture_moves

    @m.context("Test black pawn movement vectors")
    @m.it("Black pawn should have its correct movement vectors")
    def test_movement_vectors_black_pawn(self):
        expected_black_pawn_movement_vectors = [(1, 0)]
        assert all(
            [
                movement_vector in test_black_pawn._movement_vectors
                for movement_vector in expected_black_pawn_movement_vectors
            ]
        )

    @m.context("Test black pawn movement vectors")
    @m.it("Black pawn should have its correct capture vectors")
    def test_capture_vectors_black_pawn(self):
        expected_black_pawn_capture_vectors = [(1, 1), (1, -1)]
        assert all(
            [
                movement_vector in test_black_pawn._capture_vectors
                for movement_vector in expected_black_pawn_capture_vectors
            ]
        )

    @m.context("Test black pawn possible moves")
    @m.it("Black pawn should be able to move two squares only in its initial row")
    def test_initial_moves_black_pawn(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 1  # 7 in algebraic
        # Pawn at e7
        for column in range(8):
            black_pawn = Pawn(row=initial_row, column=column, is_white=False)
            test_board.squares[initial_row][column] = black_pawn
            black_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(initial_row + 1, column) in black_pawn.possible_moves
            assert indexes_to_algebraic(initial_row + 2, column) in black_pawn.possible_moves
        test_board = Board()
        test_board.init_empty_board()
        next_row = initial_row + 1
        for column in range(8):
            black_pawn = Pawn(row=next_row, column=column, is_white=False)
            test_board.squares[next_row][column] = black_pawn
            black_pawn.update_possible_moves(test_board.squares)
            assert indexes_to_algebraic(next_row + 1, column) in black_pawn.possible_moves
            assert indexes_to_algebraic(next_row + 2, column) not in black_pawn.possible_moves

    @m.context("Test black pawn possible moves")
    @m.it("If next square is blocked by a black piece, pawn shouldn't be able to move")
    def test_blocked_square_by_black_piece_black_pawn(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6
        initial_column = 4
        black_pawn = Pawn(initial_row, initial_column, False)
        blocking_black_pawn = Pawn(initial_row + 1, initial_column, False)
        test_board.init_board_with_pieces(black_pawn, blocking_black_pawn)
        black_pawn.update_possible_moves(test_board.squares)
        assert indexes_to_algebraic(initial_row + 1, initial_column) not in black_pawn.possible_moves
        assert indexes_to_algebraic(initial_row + 2, initial_column) not in black_pawn.possible_moves

    @m.context("Test black pawn possible moves")
    @m.it("If next square is blocked by a white piece, pawn shouldn't be able to capture it")
    def test_blocked_square_by_white_piece_black_pawn(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6
        initial_column = 4
        black_pawn = Pawn(initial_row, initial_column, False)
        blocking_white_pawn = Pawn(initial_row + 1, initial_column, True)
        test_board.init_board_with_pieces(black_pawn, blocking_white_pawn)
        black_pawn.update_possible_moves(test_board.squares)
        assert indexes_to_algebraic(initial_row + 1, initial_column) not in black_pawn.possible_moves
        assert indexes_to_algebraic(initial_row + 2, initial_column) not in black_pawn.possible_moves

    @m.context("Test black pawn capture moves")
    @m.it("If next square is blocked by a black piece, pawn shouldn't be able to capture it")
    def test_black_pawn_capturing_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 6
        initial_column = 4
        black_pawn = Pawn(initial_row, initial_column, False)
        white_pawn_a = Pawn(initial_row + 1, initial_column, True)
        white_pawn_b = Pawn(initial_row + 1, initial_column - 1, True)
        white_pawn_c = Pawn(initial_row + 1, initial_column + 1, True)
        test_board.init_board_with_pieces(black_pawn, white_pawn_a, white_pawn_b, white_pawn_c)
        black_pawn.update_possible_moves(test_board.squares)
        print(test_board)
        assert black_pawn.capture_moves
        assert indexes_to_algebraic(initial_row + 1, initial_column) not in black_pawn.capture_moves
        assert indexes_to_algebraic(initial_row + 1, initial_column - 1) in black_pawn.capture_moves
        assert indexes_to_algebraic(initial_row + 1, initial_column + 1) in black_pawn.capture_moves
