from typing import Tuple


def row_index_to_coordinate(row_index: int) -> str:
    return str(8 - row_index)


def row_coordinate_to_index(row_coordinate: str) -> int:
    return int(8 - int(row_coordinate))


def column_index_to_coordinate(column_index: int) -> str:
    return "abcdefgh"[column_index]


def column_coordinate_to_index(column_coordinate: str) -> int:
    return "abcdefgh".index(column_coordinate)


def indexes_to_algebraic(row_index: int, column_index: int) -> str:
    return column_index_to_coordinate(column_index) + row_index_to_coordinate(row_index)


def coordinate_to_row_column(coordinate: str) -> Tuple[int, int]:
    column_coordinate = coordinate[0]
    row_coordinate = coordinate[1]
    row_index = row_coordinate_to_index(row_coordinate)
    column_index = column_coordinate_to_index(column_coordinate)
    return row_index, column_index
