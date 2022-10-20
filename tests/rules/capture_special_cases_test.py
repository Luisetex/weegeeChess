from pytest import mark as m
from src.game import Game
from src.pieces import EnPassantPawn, Pawn


@m.describe("Test game logic special capture cases")
class TestCaptureSpecialCases:
    @m.context("Test en passant capture white to black")
    @m.it("should create an en passant pawn when moving two squares from start")
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
        print(game.board)
        print(moving_pawn.possible_moves)
        game.move_piece_to_square(moving_pawn, "e2", "e4", game.player_1, game.player_2)
        assert game.board.squares[4][4] == moving_pawn
        assert isinstance(game.board.squares[6][4], EnPassantPawn)
