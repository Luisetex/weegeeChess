from typing import List, Tuple

from .board import Board
from .exceptions import DiscoveredCheckException, ImpossibleMoveException, PieceNotFoundException
from .parser import parse_command
from .pieces import King, Pawn, Piece
from .player import Player
from .utils import algebraic_to_indexes, indexes_to_algebraic


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces = self._get_all_pieces()
        self.player_1 = Player(is_white=True, all_pieces=self.pieces)
        self.player_2 = Player(is_white=False, all_pieces=self.pieces)

    def play_game(self):
        print("Let the game begin!")
        print(self.board)
        while True:
            self._player_turn(self.player_1, self.player_2)
            self._player_turn(self.player_2, self.player_1)

    def _get_all_pieces(self) -> List[Piece]:
        pieces: List[Piece] = []
        for row in self.board.squares:
            for square in row:
                if isinstance(square, Piece):
                    pieces.append(square)
        return pieces

    def get_origin_square_player_piece(self, player: Player, origin_algebraic: str) -> Piece | None:
        row_index, column_index = algebraic_to_indexes(origin_algebraic)
        origin_square = self.board.squares[row_index][column_index]
        if origin_square:
            if origin_square.is_white == player.is_white:
                return origin_square
        return None

    def _player_turn(self, attacking_player: Player, defending_player: Player):
        turn_over = False
        while not turn_over:
            self._update_all_player_moves(attacking_player)
            self._update_all_player_moves(defending_player)
            attacking_color = "White" if attacking_player.is_white else "Black"
            print(
                f"{attacking_color}'s turn!. Introduce your move in the following way: origin square destination square"
            )
            move = input()
            origin_square, destination_square = parse_command(move)
            available_piece = self.get_origin_square_player_piece(attacking_player, origin_square)
            try:
                if available_piece:
                    self._move_piece(attacking_player, defending_player, origin_square, destination_square)
                    turn_over = True
                    print(self.board)
                else:
                    print("Cuidaaao")
            except (DiscoveredCheckException, ImpossibleMoveException) as exception:
                print(f"Careful! {str(exception)}")

    def _get_square_from_algebraic(self, algebraic_square: str) -> Piece | None:
        row_index, column_index = algebraic_to_indexes(algebraic_square)
        return self.board.get_square_from_row_column(row_index, column_index)

    def _update_all_player_moves(self, player: Player):
        for piece in player.own_pieces:
            piece.update_possible_moves(self.board.squares)

    def _move_piece_to_square(
        self,
        player_piece: Piece,
        origin_square: str,
        destination_square: str,
        attacking_player: Player,
        defending_player: Player,
    ):
        origin_row_index, origin_column_index = algebraic_to_indexes(origin_square)
        dest_row_index, dest_column_index = algebraic_to_indexes(destination_square)
        player_square = self.board.squares[origin_row_index][origin_column_index]
        opponent_square = self.board.squares[dest_row_index][dest_column_index]
        if isinstance(player_square, Pawn):
            if opponent_square:
                if destination_square not in player_square.capture_moves:
                    raise ImpossibleMoveException(origin_square, destination_square)
        self.board.squares[dest_row_index][dest_column_index] = player_piece
        player_piece.row = dest_row_index
        player_piece.column = dest_row_index
        self.board.squares[origin_row_index][origin_column_index] = None
        self._update_all_player_moves(attacking_player)
        self._update_all_player_moves(defending_player)
        discovered_check_pieces = self._is_king_checked(
            attacking_player=defending_player, defending_player=attacking_player
        )
        if discovered_check_pieces:
            self.board.squares[origin_row_index][origin_column_index] = player_square
            self.board.squares[dest_row_index][dest_column_index] = opponent_square
            raise DiscoveredCheckException(discovered_check_pieces)

    def _is_king_checked(self, attacking_player: Player, defending_player: Player):
        king = [piece for piece in defending_player.own_pieces if isinstance(piece, King)][0]
        king_row_index, king_column_index = king.row, king.column
        king_algebraic_square = indexes_to_algebraic(king_row_index, king_column_index)
        return [piece for piece in attacking_player.own_pieces if king_algebraic_square in piece.possible_moves]

    def _move_piece(
        self, attacking_player: Player, defending_player: Player, origin_square: str, destination_square: str
    ):
        player_piece = self.get_origin_square_player_piece(attacking_player, origin_square)
        if player_piece:
            if destination_square in player_piece.possible_moves:
                self._move_piece_to_square(
                    player_piece, origin_square, destination_square, attacking_player, defending_player
                )
            else:
                raise ImpossibleMoveException(origin_square, destination_square)
