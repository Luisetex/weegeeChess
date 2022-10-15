from typing import Tuple

from .board import Board
from .parser import parse_command
from .pieces import Piece
from .player import Player
from .utils import algebraic_to_indexes


class Game:
    def __init__(self):
        self.board = Board()
        self.player_1 = Player(is_white=True, squares=self.board.squares)
        self.player_2 = Player(is_white=False, squares=self.board.squares)

    def play_game(self):
        print("Let the game begin!")
        print(self.board)
        while True:
            print(
                "White's turn!. Introduce your move in the following way: origin square destination square"
            )
            move = input()
            origin_square, destination_square = parse_command(move)
            is_origin_available, available_piece = self._is_origin_square_available_for_player(
                self.player_1, origin_square
            )
            if available_piece:
                available_piece.update_possible_moves(self.board.squares)
                is_possible = destination_square in available_piece.possible_moves
                print(f"is possible to move? {is_possible}")

    def _is_origin_square_available_for_player(
        self, player: Player, origin_square: str
    ) -> Tuple[bool, Piece | None]:
        row_index, column_index = algebraic_to_indexes(origin_square)
        for player_piece in player.own_pieces:
            if row_index == player_piece.row and column_index == player_piece.column:
                return True, player_piece
        return False, None
