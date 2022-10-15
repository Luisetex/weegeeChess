from __future__ import annotations

from typing import List, Tuple

from .utils import coordinate_to_row_column, indexes_to_algebraic

WHITE_KING = "♔"
WHITE_QUEEN = "♕"
WHITE_ROOK = "♖"
WHITE_BISHOP = "♗"
WHITE_KNIGHT = "♘"
WHITE_PAWN = "♙"

BLACK_KING = "♚"
BLACK_QUEEN = "♛"
BLACK_ROOK = "♜"
BLACK_BISHOP = "♝"
BLACK_KNIGHT = "♞"
BLACK_PAWN = "♟"


class Piece:
    def __init__(self, char: str, is_white: bool, row: int, column: int, is_ranged: bool = True):
        self.char = char
        self.is_white = is_white
        self.row = row
        self.column = column
        self.has_moved: bool = False
        self.possible_moves: List[str] = []
        self.is_ranged = is_ranged
        self._movements: List[Tuple[int, int]]

    def __str__(self) -> str:
        return self.char

    def __repr__(self) -> str:
        return f"Piece: {self.char}. Row: {self.row}. Column: {self.column}. Algebraic: {indexes_to_algebraic(self.row, self.column)}"

    def _check_boundary(self, new_row_pos: int, new_column_pos: int) -> bool:
        return 0 <= new_row_pos <= 7 and 0 <= new_column_pos <= 7

    def _check_destination_is_origin(self, new_row_pos: int, new_column_pos: int) -> bool:
        return new_row_pos == self.row and new_column_pos == self.column

    def _is_destination_square_valid(
        self, destination_row: int, destination_column: int, board: List[List[Piece | None]]
    ) -> bool:
        destination_square = board[destination_row][destination_column]
        if isinstance(destination_square, Piece):
            if destination_square.is_white != self.is_white:
                return True
        else:
            return True
        return False

    def get_possible_moves(self, board: List[List[Piece | None]]):
        number_of_steps = 7 if self.is_ranged else 1
        possible_moves: List[str] = []
        for movement in self._movements:
            candidate_row = self.row
            candidate_column = self.column
            for _ in range(number_of_steps):
                candidate_row += movement[0]
                candidate_column += movement[1]
                if self._check_boundary(candidate_row, candidate_column):
                    if self._is_destination_square_valid(candidate_row, candidate_column, board):
                        possible_moves.append(indexes_to_algebraic(candidate_row, candidate_column))
                else:
                    break
        self.possible_moves = possible_moves


class Pawn(Piece):
    def __init__(self, row: int, column: int, is_white: bool):
        char = WHITE_PAWN if is_white else BLACK_PAWN
        super().__init__(char=char, is_white=is_white, row=row, column=column, is_ranged=False)
        self._movements = [(1, 0)] if self.is_white else [(-1, 0)]


class King(Piece):
    def __init__(self, row: int, column: int, is_white: bool):
        char = WHITE_KING if is_white else BLACK_KING
        super().__init__(char=char, is_white=is_white, row=row, column=column, is_ranged=False)
        self._movements = [(-1, -1), (-1, 1), (-1, 0), (1, -1), (1, 1), (1, 0), (0, -1), (0, 1)]


class Queen(Piece):
    def __init__(self, row: int, column: int, is_white: bool):
        char = WHITE_QUEEN if is_white else BLACK_QUEEN
        super().__init__(char=char, is_white=is_white, row=row, column=column)
        self._movements = [(-1, -1), (-1, 1), (-1, 0), (1, -1), (1, 1), (1, 0), (0, -1), (0, 1)]


class Rook(Piece):
    def __init__(self, row: int, column: int, is_white: bool):
        char = WHITE_ROOK if is_white else BLACK_ROOK
        super().__init__(char=char, is_white=is_white, row=row, column=column)
        self._movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Bishop(Piece):
    def __init__(self, row: int, column: int, is_white: bool):
        char = WHITE_BISHOP if is_white else BLACK_BISHOP
        super().__init__(char=char, is_white=is_white, row=row, column=column)
        self._movements = [(1, 1), (-1, -1), (1, -1), (-1, 1)]


class Knight(Piece):
    def __init__(self, row: int, column: int, is_white: bool):
        char = WHITE_KNIGHT if is_white else BLACK_KNIGHT
        super().__init__(char=char, is_white=is_white, row=row, column=column, is_ranged=False)
        self._movements = [(2, -1), (2, 1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
