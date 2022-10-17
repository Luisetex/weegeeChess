from typing import List

from .pieces import Piece


class DiscoveredCheckException(Exception):
    def __init__(self, check_pieces: List[Piece]):
        super().__init__(f"Discovered King! Checked by {check_pieces}")


class ImpossibleMoveException(Exception):
    def __init__(self, origin_square_algebraic: str, destination_square_algebraic: str):
        super().__init__(f"Cannot move from {origin_square_algebraic} to {destination_square_algebraic}")


class PieceNotFoundException(Exception):
    def __init__(self, origin_square_algebraic: str):
        super().__init__(f"Cannot find piece at {origin_square_algebraic}")
