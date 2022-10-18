from copy import copy
from typing import List

from .pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from .utils import row_index_to_algebraic

BLACK_SQUARE = "█"
WHITE_SQUARE = " "


class Board:
    squares: List[List[Piece | None]]

    def __init__(self):
        self.init_board()

    def __str__(self):
        text: str = ""
        for row_index, row in enumerate(self.squares):
            for column_index, square in enumerate(row):
                if column_index == 0:
                    text += row_index_to_algebraic(row_index) + " "
                if square:
                    text += square.char + " "
                else:
                    if (row_index + column_index) % 2 == 0:
                        text += WHITE_SQUARE + " "
                    else:
                        text += BLACK_SQUARE + " "
            text += "\n"
        text += "  a b c d e f g h\n"
        return text

    def init_board(self):
        self.squares = []
        for _ in range(8):
            self.squares.append([None] * 8)
        # PAWNS
        for column_index, _ in enumerate(self.squares[1]):
            self.squares[1][column_index] = Pawn(1, column_index, False)
        for column_index, _ in enumerate(self.squares[6]):
            self.squares[6][column_index] = Pawn(6, column_index, True)
        # ROOKS
        self.squares[0][0] = Rook(0, 0, False)
        self.squares[0][7] = Rook(0, 7, False)
        self.squares[7][0] = Rook(7, 0, True)
        self.squares[7][7] = Rook(7, 7, True)
        # KNIGHTS
        self.squares[0][1] = Knight(0, 1, False)
        self.squares[0][6] = Knight(0, 6, False)
        self.squares[7][1] = Knight(7, 1, True)
        self.squares[7][6] = Knight(7, 6, True)
        # BISHOPS
        self.squares[0][2] = Bishop(0, 2, False)
        self.squares[0][5] = Bishop(0, 5, False)
        self.squares[7][2] = Bishop(7, 2, True)
        self.squares[7][5] = Bishop(7, 5, True)
        # QUEENS
        self.squares[0][3] = Queen(0, 3, False)
        self.squares[7][3] = Queen(7, 3, True)
        # KINGS
        self.squares[0][4] = King(0, 4, False)
        self.squares[7][4] = King(7, 4, True)

    def init_board_with_pieces(self, *pieces: Piece):
        for piece in pieces:
            self.squares[piece.row][piece.column] = piece

    def clear_board(self):
        for row in self.squares:
            for square in row:
                square = None

    def get_square_from_row_column(self, row_index: int, column_index: int) -> Piece | None:
        return self.squares[row_index][column_index]

    def update_board(self):
        for row_index, row in enumerate(self.squares):
            for column_index, origin_square in enumerate(row):
                if origin_square:
                    if origin_square.row != row_index or origin_square.column != column_index:
                        destiny_square = self.squares[origin_square.row][origin_square.column]
                        if destiny_square.piece:
                            self._update_squares(origin_square, destiny_square)
                        elif destiny_square.piece == None:
                            self._update_squares(origin_square, destiny_square)

    def _update_squares(self, origin_square: Piece | None, destiny_square: Piece | None):
        destiny_square = copy(origin_square)
        origin_square = None
