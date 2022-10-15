from src.board import Board

BLACK_SQUARE = "█"
WHITE_SQUARE = " "


if __name__ == "__main__":
    board = Board()
    print(board)
    board.squares[0][0].get_possible_moves(board.squares)
    board.update_board()
    print("\n\nMoving Pawn")
    print(board)
    print(board)
