from get_board import get_board
from render_board import render_board

def main():
    # Train / load pre-trained data

    # Create board representation from camera input
    board = get_board()

    # Read board to screen
    render_board(board)

    # Show live camera feed + chessboard on screen

if __name__ == "__main__":
    main()
