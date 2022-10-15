from copy import copy
from typing import List

from .pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from .utils import indexes_to_algebraic, row_index_to_coordinate

BLACK_SQUARE = "█"
WHITE_SQUARE = " "


class Board:
    squares: List[List[Piece | None]]

    def __init__(self):
        self._init_board()

    def __str__(self):
        text: str = ""
        for row_index, row in enumerate(self.squares):
            for column_index, square in enumerate(row):
                if column_index == 0:
                    text += row_index_to_coordinate(row_index) + " "
                if square:
                    text += square.char
                else:
                    if (row_index + column_index) % 2 == 0:
                        text += WHITE_SQUARE
                    else:
                        text += BLACK_SQUARE
            text += "\n"
        text += "  abcdefgh\n"
        return text

    def _init_board(self):
        self.squares = []
        for _ in range(8):
            self.squares.append([None] * 8)
        # PAWNS
        #        for column_index, _ in enumerate(self.board[1]):
        #           self.board[1][column_index] = Pawn(1, column_index, "black")
        #        for column_index, _ in enumerate(self.board[6]):
        #            self.board[6][column_index] = Pawn(6, column_index, "white")
        # ROOKS
        self.squares[0][0] = Rook(0, 0, "black")
        self.squares[0][7] = Rook(0, 7, "black")
        self.squares[7][0] = Rook(7, 0, "white")
        self.squares[7][7] = Rook(7, 7, "white")
        # KNIGHTS
        self.squares[0][1] = Knight(0, 1, "black")
        self.squares[0][6] = Knight(0, 6, "black")
        self.squares[7][1] = Knight(7, 1, "white")
        self.squares[7][6] = Knight(7, 6, "white")
        # BISHOPS
        self.squares[0][2] = Bishop(0, 2, "black")
        self.squares[0][5] = Bishop(0, 5, "black")
        self.squares[7][2] = Bishop(7, 2, "white")
        self.squares[7][5] = Bishop(7, 5, "white")
        # QUEENS
        self.squares[0][3] = Queen(0, 3, "black")
        self.squares[7][3] = Queen(7, 3, "white")
        # KINGS
        self.squares[0][4] = King(0, 4, "black")
        self.squares[7][4] = King(7, 4, "white")

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
