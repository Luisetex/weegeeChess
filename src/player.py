from typing import List

from .pieces import Piece


class Player:
    pieces: List[Piece]

    def __init__(self, is_white: bool, squares: List[List[Piece | None]]):
        self.is_white = is_white
        self.name = "White" if self.is_white else "Black"
        self.squares = squares
        self.own_pieces: List[Piece] = []
        self.update_own_pieces()

    def update_own_pieces(self):
        own_pieces: List[Piece] = []
        for row in self.squares:
            for candidate_piece in row:
                if candidate_piece and candidate_piece.is_white == self.is_white:
                    own_pieces.append(candidate_piece)
        self.own_pieces = own_pieces
