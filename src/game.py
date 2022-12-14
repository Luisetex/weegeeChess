from typing import List

from .board import Board
from .exceptions import DiscoveredCheckException, ImpossibleMoveException
from .parser import parse_command
from .pieces import EnPassantPawn, King, Pawn, Piece
from .player import Player
from .utils import algebraic_to_indexes, indexes_to_algebraic


class Game:
    def __init__(self):
        self.board = Board()
        self.board.init_board()
        self.pieces = self._get_all_pieces()
        self.player_1 = Player(is_white=True, all_pieces=self.pieces)
        self.player_2 = Player(is_white=False, all_pieces=self.pieces)
        self.checkmate = False
        self.stalemate = False

    def play_game(self):
        print("Let the game begin!")
        print(self.board)
        while True:
            self._player_turn(self.player_1, self.player_2)
            if self.checkmate:
                break
            self._player_turn(self.player_2, self.player_1)
            if self.checkmate or self.stalemate:
                break
        print("Checkmate") if self.checkmate else print("Stalemate")

    def _player_turn(self, attacking_player: Player, defending_player: Player):
        turn_over = False
        while not turn_over:
            self._remove_en_passant_pawn(attacking_player)
            self.update_all_player_moves(attacking_player)
            self.update_all_player_moves(defending_player)
            self._remove_illegal_moves(attacking_player, defending_player)
            has_player_available_moves = self._has_player_available_moves(attacking_player)
            opossite_checking_pieces = self._get_opposite_checking_pieces(
                defending_player, attacking_player
            )
            if opossite_checking_pieces:
                if has_player_available_moves:
                    self.checkmate = True
                    break
            if has_player_available_moves:
                self.stalemate = True
                break

            attacking_color = "White" if attacking_player.is_white else "Black"
            print(
                f"{attacking_color}'s turn!. Introduce your move in the following way: origin square destination square"
            )
            move = input()
            origin_square, destination_square = parse_command(move)
            available_piece = self._get_origin_square_player_piece(attacking_player, origin_square)
            try:
                if available_piece:
                    self.move_piece(
                        attacking_player,
                        available_piece,
                        defending_player,
                        origin_square,
                        destination_square,
                    )
                    turn_over = True
                    print(self.board)
                else:
                    print(f"No piece available at {origin_square}")
            except (DiscoveredCheckException, ImpossibleMoveException) as exception:
                print(f"Careful! {str(exception)}")

    def update_all_player_moves(self, player: Player):
        for piece in player.own_pieces:
            piece.update_possible_moves(self.board.squares)

    def _remove_illegal_moves(self, attacking_player: Player, defending_player: Player):
        for piece in attacking_player.own_pieces:
            for move in piece.capture_moves + piece.possible_moves:
                if self._is_move_illegal(attacking_player, defending_player, piece, move):
                    if move in piece.possible_moves:
                        piece.possible_moves.remove(move)
                    else:
                        piece.capture_moves.remove(move)

    def _is_move_illegal(
        self, attacking_player: Player, defending_player: Player, piece: Piece, possible_move: str
    ):
        attacking_player_king = [
            piece for piece in attacking_player.own_pieces if isinstance(piece, King)
        ][0]
        attacking_player_king_algebraic = indexes_to_algebraic(
            attacking_player_king.row, attacking_player_king.column
        )
        original_square_row = piece.row
        original_square_column = piece.column
        destination_square_row, destination_square_column = algebraic_to_indexes(possible_move)
        destination_square_content = self.board.squares[destination_square_row][
            destination_square_column
        ]
        self.board.squares[destination_square_row][destination_square_column] = piece
        self.board.squares[original_square_row][original_square_column] = destination_square_content
        if isinstance(piece, King):
            attacking_player_king_algebraic = possible_move
        self.update_all_player_moves(defending_player)
        is_illegal = any(
            [
                attacking_player_king_algebraic in (piece.possible_moves + piece.capture_moves)
                for piece in defending_player.own_pieces
            ]
        )
        self.board.squares[destination_square_row][
            destination_square_column
        ] = destination_square_content
        self.board.squares[original_square_row][original_square_column] = piece
        self.update_all_player_moves(defending_player)
        return is_illegal

    def move_piece(
        self,
        attacking_player: Player,
        attacking_player_piece: Piece,
        defending_player: Player,
        origin_square: str,
        destination_square: str,
    ):
        if (
            destination_square in attacking_player_piece.possible_moves
            or destination_square in attacking_player_piece.capture_moves
        ):
            self.move_piece_to_square(
                attacking_player_piece,
                origin_square,
                destination_square,
                attacking_player,
                defending_player,
            )
        else:
            raise ImpossibleMoveException(origin_square, destination_square)

    def _get_origin_square_player_piece(
        self, player: Player, origin_algebraic: str
    ) -> Piece | None:
        row_index, column_index = algebraic_to_indexes(origin_algebraic)
        origin_square = self.board.squares[row_index][column_index]
        if origin_square:
            if origin_square.is_white == player.is_white:
                return origin_square
        return None

    def move_piece_to_square(
        self,
        attacking_player_piece: Piece,
        origin_square: str,
        destination_square: str,
        attacking_player: Player,
        defending_player: Player,
    ):
        origin_row_index, origin_column_index = algebraic_to_indexes(origin_square)
        dest_row_index, dest_column_index = algebraic_to_indexes(destination_square)
        opponent_square = self.board.squares[dest_row_index][dest_column_index]

        if opponent_square:
            if not (
                destination_square in attacking_player_piece.capture_moves
                or destination_square in attacking_player_piece.possible_moves
            ):
                raise ImpossibleMoveException(origin_square, destination_square)
            self._remove_piece_from_player(defending_player, opponent_square)

        self.board.squares[dest_row_index][dest_column_index] = attacking_player_piece
        attacking_player_piece.row = dest_row_index
        attacking_player_piece.column = dest_column_index
        if isinstance(attacking_player_piece, Pawn):
            if (
                dest_column_index == origin_column_index
                and abs(dest_row_index - origin_row_index) == 2
            ):
                en_passant_pawn_column = origin_column_index
                en_passant_pawn_row = (
                    origin_row_index - 1
                    if attacking_player_piece.is_white
                    else origin_row_index + 1
                )
                en_passant_pawn = EnPassantPawn(attacking_player_piece)
                self.board.squares[en_passant_pawn_row][en_passant_pawn_column] = en_passant_pawn
                attacking_player.own_pieces.append(en_passant_pawn)

        self.board.squares[origin_row_index][origin_column_index] = None
        self.update_all_player_moves(attacking_player)
        self.update_all_player_moves(defending_player)

    def _get_all_pieces(self) -> List[Piece]:
        pieces: List[Piece] = []
        for row in self.board.squares:
            for square in row:
                if isinstance(square, Piece):
                    pieces.append(square)
        return pieces

    def _get_square_from_algebraic(self, algebraic_square: str) -> Piece | None:
        row_index, column_index = algebraic_to_indexes(algebraic_square)
        return self.board.get_square_from_row_column(row_index, column_index)

    def _remove_piece_from_player(self, player: Player, piece: Piece):
        if isinstance(piece, EnPassantPawn):
            original_pawn = piece.original_pawn
            player.own_pieces.pop(player.own_pieces.index(original_pawn))
            self.board.squares[original_pawn.row][original_pawn.column] = None
        player.own_pieces.pop(player.own_pieces.index(piece))

    def _get_opposite_checking_pieces(
        self, attacking_player: Player, defending_player: Player
    ) -> List[Piece]:
        king = [piece for piece in defending_player.own_pieces if isinstance(piece, King)][0]
        king_row_index, king_column_index = king.row, king.column
        king_algebraic_square = indexes_to_algebraic(king_row_index, king_column_index)
        return [
            piece
            for piece in attacking_player.own_pieces
            if king_algebraic_square in piece.possible_moves
        ]

    def _has_player_available_moves(self, player: Player) -> bool:
        for piece in player.own_pieces:
            available_moves = piece.capture_moves + piece.possible_moves
            if available_moves:
                return False
        return True

    def _remove_en_passant_pawn(self, player: Player):
        en_passant_pawn: Piece | None = None
        for piece in player.own_pieces:
            en_passant_pawn = piece if isinstance(piece, EnPassantPawn) else None
        if en_passant_pawn:
            self.board.squares[en_passant_pawn.row][en_passant_pawn.column] = None
            player.own_pieces.remove(en_passant_pawn)
