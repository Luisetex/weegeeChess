from typing import List

from .pieces import Piece


class Player:
    def __init__(self, is_white: bool, all_pieces: List[Piece]):
        self.is_white = is_white
        self.name = "White" if self.is_white else "Black"
        self.own_pieces = self._get_own_pieces(all_pieces)

    def _get_own_pieces(self, pieces: List[Piece]) -> List[Piece]:
        return [piece for piece in pieces if piece.is_white == self.is_white]

    def get_all_available_moves(self):
        available_moves: List[str] = []
        for piece in self.own_pieces:
            available_moves += (piece.capture_moves + piece.possible_moves)
        return available_moves

    """ def update_own_pieces(self):
        own_pieces: List[Piece] = []
        for row in self.squares:
            for candidate_piece in row:
                if candidate_piece and candidate_piece.is_white == self.is_white:
                    own_pieces.append(candidate_piece)
        self.own_pieces = own_pieces
 """
