from pytest import mark as m
from src.board import Board
from src.pieces import Bishop

test_board = Board().init_empty_board()
test_white_bishop = Bishop(row=6, column=4, is_white=True)
test_black_bishop = Bishop(row=2, column=4, is_white=False)


@m.describe("Test Bishop Logic")
class TestBishopk:
    @m.context("Test bishop movement vectors")
    @m.it("Bishop should have its correct movement vectors")
    def test_movement_vectors_white_bishop(self):
        expected_white_bishop_movement_vectors = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        assert all(
            [
                movement_vector in test_white_bishop._movement_vectors
                for movement_vector in expected_white_bishop_movement_vectors
            ]
        )

    @m.context("Test bishop possible moves")
    @m.it("Bishop should be able to move as much as possible according to its vectors")
    def test_empty_board_bishop_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        bishop = Bishop(row=initial_row, column=initial_column, is_white=True)
        test_board.init_board_with_pieces(bishop)
        bishop.update_possible_moves(test_board.squares)
        expected_possible_moves = ["f5", "g6", "h7", "d5", "c6", "b7", "a8", "d3", "c2", "b1", "f3", "g2", "h1"]
        assert len(bishop.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in bishop.possible_moves

    @m.context("Test bishop possible moves")
    @m.it("Bishop should'n be able to move where a piece of the same color is")
    def test_blocking_white_piece_bishop_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        bishop = Bishop(row=initial_row, column=initial_column, is_white=True)
        blocking_bishop_g6 = Bishop(row=initial_row - 2, column=6, is_white=True)
        blocking_bishop_c2 = Bishop(row=initial_row + 2, column=2, is_white=True)
        test_board.init_board_with_pieces(bishop, blocking_bishop_g6, blocking_bishop_c2)
        bishop.update_possible_moves(test_board.squares)
        expected_possible_moves = ["f5", "d5", "c6", "b7", "a8", "d3", "f3", "g2", "h1"]
        assert len(bishop.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in bishop.possible_moves

    @m.context("Test bishop possible moves")
    @m.it("Bishop should be able to move where a piece of the opposite color is")
    def test_capturing_white_piece_bishop_moves(self):
        test_board = Board()
        test_board.init_empty_board()
        initial_row = 4  # 4 in algebraic
        initial_column = 4  # e in algebraic
        bishop = Bishop(row=initial_row, column=initial_column, is_white=True)
        blocking_bishop_g6 = Bishop(row=initial_row - 2, column=6, is_white=False)
        opposing_bishop_c2 = Bishop(row=initial_row + 2, column=2, is_white=True)
        test_board.init_board_with_pieces(bishop, blocking_bishop_g6, opposing_bishop_c2)
        bishop.update_possible_moves(test_board.squares)
        print(test_board)
        print(bishop.possible_moves)
        expected_possible_moves = ["f5", "d5", "c6", "b7", "a8", "d3", "f3", "g2", "h1", "g6"]
        assert len(bishop.possible_moves) == len(expected_possible_moves)
        for expected_possible_move in expected_possible_moves:
            assert expected_possible_move in bishop.possible_moves
