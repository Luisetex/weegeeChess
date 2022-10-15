from typing import Tuple


def parse_command(command: str) -> Tuple[str, str]:
    origin_square, destination_square = command.split(" ")
    return origin_square, destination_square
