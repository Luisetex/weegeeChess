from pytest import mark as m
from src.board import Board
from src.pieces import Knight

test_board = Board().init_empty_board()
test_white_knight = Knight(row=6, column=4, is_white=True)
test_black_knight = Knight(row=2, column=4, is_white=False)


@m.describe("Test Knight Logic")
class TestKnightk:
    @m.context("Test knight movement vectors")
    @m.it("Knight should have its correct movement vectors")
    def test_movement_vectors_white_knight(self):
        expected_white_knight_movement_vectors = [
            (2, -1),
            (2, 1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ]
        assert all(
            [
                movement_vector in test_white_knight._movement_vectors
                for movement_vector in expected_white_knight_movement_vectors
            ]
        )

    @m.context("Test knight possible moves")
    @m.it("Knight should be able to move as much as possible according to its vectors")
    def test_empty_board_knight_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        knight = Knight(row=initial_row, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(knight)
        knight.update_possible_moves(test_board.squares)
        expected_possible_moves = ["d6", "f6", "d2", "f2", "c5", "c3", "g5", "g3"]
        assert len(knight.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in knight.possible_moves

    @m.context("Test knight possible moves")
    @m.it("Knight should'n be able to move out of bounds")
    def test_out_of_bounds_knight_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 7  # 1 in algebraic
        initial_column = 0  # a in algebraic
        knight = Knight(row=initial_row, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(knight)
        knight.update_possible_moves(test_board.squares)
        expected_possible_moves = ["b3", "c2"]
        assert len(knight.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in knight.possible_moves

    @m.context("Test knight possible moves")
    @m.it("Knight should'n be able to move where a piece of the same color is")
    def test_blocking_white_piece_knight_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        knight = Knight(row=initial_row, column=initial_column, is_white=True)
        blocking_knight_d6 = Knight(row=initial_row - 2, column=3, is_white=True)
        blocking_knight_c3 = Knight(row=initial_row + 1, column=2, is_white=True)
        test_board.init_board_with_pieces(knight, blocking_knight_c3, blocking_knight_d6)
        knight.update_possible_moves(test_board.squares)
        expected_possible_moves = ["f6", "d2", "f2", "c5", "g5", "g3"]
        assert len(knight.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in knight.possible_moves

    @m.context("Test knight possible moves")
    @m.it("Knight should be able to move where a piece of the opposite color is")
    def test_capturing_white_piece_knight_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        knight = Knight(row=initial_row, column=initial_column, is_white=True)
        blocking_knight_d6 = Knight(row=initial_row - 2, column=3, is_white=False)
        blocking_knight_c3 = Knight(row=initial_row + 1, column=2, is_white=True)
        test_board.init_board_with_pieces(knight, blocking_knight_c3, blocking_knight_d6)
        knight.update_possible_moves(test_board.squares)
        expected_possible_moves = ["f6", "d2", "f2", "c5", "g5", "g3", "d6"]
        assert len(knight.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in knight.possible_moves
