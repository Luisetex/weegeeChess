from pytest import mark as m
from src.game import Game
from src.pieces import EnPassantPawn, Pawn
from src.utils import algebraic_to_indexes


@m.describe("Test game logic special capture cases")
class TestCaptureSpecialCases:
    @m.context("Test en passant capture white to black")
    @m.it("should create a en passant pawn when moving two squares from start")
    def test_en_passant_capture_white_to_black(self):
        game = Game()
        game.board.init_empty_board()
        moving_pawn = Pawn(6, 4, True)
        defending_pawn = Pawn(4, 3, False)
        game.player_1.own_pieces = [moving_pawn]
        game.player_2.own_pieces = [defending_pawn]
        game.board.init_board_with_pieces(moving_pawn, defending_pawn)
        game.update_all_player_moves(game.player_1)
        game.update_all_player_moves(game.player_2)
        game.move_piece_to_square(moving_pawn, "e2", "e4", game.player_1, game.player_2)
        dest_row_index, dest_column_index = algebraic_to_indexes("e4")
        assert game.board.squares[dest_row_index][dest_column_index] == moving_pawn
        assert isinstance(game.board.squares[dest_row_index + 1][dest_column_index], EnPassantPawn)

    @m.context("Test en passant capture black to white")
    @m.it("should create a en passant pawn when moving two squares from start")
    def test_en_passant_capture_black_to_white(self):
        game = Game()
        game.board.init_empty_board()
        moving_pawn = Pawn(1, 3, False)
        defending_pawn = Pawn(3, 4, True)
        game.player_1.own_pieces = [defending_pawn]
        game.player_2.own_pieces = [moving_pawn]
        game.board.init_board_with_pieces(moving_pawn, defending_pawn)
        print(game.board)
        game.update_all_player_moves(game.player_1)
        game.update_all_player_moves(game.player_2)
        game.move_piece_to_square(moving_pawn, "d7", "d5", game.player_2, game.player_1)
        dest_row_index, dest_column_index = algebraic_to_indexes("d5")
        assert game.board.squares[dest_row_index][dest_column_index] == moving_pawn
        assert isinstance(game.board.squares[dest_row_index - 1][dest_column_index], EnPassantPawn)
