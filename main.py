from src.game import Game

BLACK_SQUARE = "█"
WHITE_SQUARE = " "


if __name__ == "__main__":
    """board = Board()
    print(board)
    board.squares[1][4].update_possible_moves(board.squares)
    board.update_board()
    print("\n\nMoving Pawn")
    print(board)
    print(board)"""
    game = Game()
    game.play_game()
