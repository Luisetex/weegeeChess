from pytest import mark as m
from src.board import Board
from src.pieces import Queen

test_board = Board().init_empty_board()
test_white_queen = Queen(row=6, column=4, is_white=True)
test_black_queen = Queen(row=2, column=4, is_white=False)


@m.describe("Test Queen Logic")
class TestQueenk:
    @m.context("Test queen movement vectors")
    @m.it("Queen should have its correct movement vectors")
    def test_movement_vectors_white_queen(self):
        expected_white_queen_movement_vectors = [(-1, -1), (-1, 1), (-1, 0), (1, -1), (1, 1), (1, 0), (0, -1), (0, 1)]
        assert all(
            [
                movement_vector in test_white_queen._movement_vectors
                for movement_vector in expected_white_queen_movement_vectors
            ]
        )

    @m.context("Test queen possible moves")
    @m.it("Queen should be able to move as much as possible according to its vectors")
    def test_empty_board_queen_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        queen = Queen(row=initial_row, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(queen)
        queen.update_possible_moves(test_board.squares)
        expected_possible_moves_same_column = ["e1", "e2", "e3", "e5", "e6", "e7", "e8"]
        expected_possible_moves_same_row = ["a4", "b4", "c4", "d4", "f4", "g4", "h4"]
        expected_possible_moves_diagonals = [
            "f5",
            "g6",
            "h7",
            "d5",
            "c6",
            "b7",
            "a8",
            "d3",
            "c2",
            "b1",
            "f3",
            "g2",
            "h1",
        ]
        expected_possible_moves = (
            expected_possible_moves_same_column + expected_possible_moves_same_row + expected_possible_moves_diagonals
        )
        assert len(queen.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in queen.possible_moves

    @m.context("Test queen possible moves")
    @m.it("Queen shouldn't be able to move where a piece of the same color is")
    def test_blocqueen_white_piece_queen_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        queen = Queen(row=initial_row, column=initial_column, is_white=True)
        blocqueen_queen_d5 = Queen(row=initial_row - 1, column=initial_column - 1, is_white=True)
        blocqueen_queen_f3 = Queen(row=initial_row + 1, column=initial_column + 1, is_white=True)
        test_board.init_board_with_pieces(queen, blocqueen_queen_d5, blocqueen_queen_f3)
        queen.update_possible_moves(test_board.squares)
        expected_possible_moves_same_column = ["e1", "e2", "e3", "e5", "e6", "e7", "e8"]
        expected_possible_moves_same_row = ["a4", "b4", "c4", "d4", "f4", "g4", "h4"]
        expected_possible_moves_diagonals = [
            "f5",
            "g6",
            "h7",
            "d3",
            "c2",
            "b1",
        ]
        expected_possible_moves = (
            expected_possible_moves_same_column + expected_possible_moves_same_row + expected_possible_moves_diagonals
        )
        assert len(queen.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in queen.possible_moves

    @m.context("Test queen possible moves")
    @m.it("Queen should be able to move where a piece of the opposite color is")
    def test_capturing_white_piece_queen_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        queen = Queen(row=initial_row, column=initial_column, is_white=True)
        blocqueen_queen_d5 = Queen(row=initial_row - 1, column=initial_column - 1, is_white=True)
        opposing_queen_f3 = Queen(row=initial_row + 1, column=initial_column + 1, is_white=False)
        test_board.init_board_with_pieces(queen, blocqueen_queen_d5, opposing_queen_f3)
        queen.update_possible_moves(test_board.squares)
        expected_possible_moves_same_column = ["e1", "e2", "e3", "e5", "e6", "e7", "e8"]
        expected_possible_moves_same_row = ["a4", "b4", "c4", "d4", "f4", "g4", "h4"]
        expected_possible_moves_diagonals = ["f5", "g6", "h7", "d3", "c2", "b1", "f3"]
        expected_possible_moves = (
            expected_possible_moves_same_column + expected_possible_moves_same_row + expected_possible_moves_diagonals
        )
        assert len(queen.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in queen.possible_moves
