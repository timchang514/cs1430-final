from get_board import get_board
from render_board import *
from tkinter import Tk
from threading import Thread, Lock
from gui import *

def gui_loop():
    root = Tk()

    mt_board = svg_to_img(new_board())
    my_gui = ChessGUI(root, mt_board)

    # Important: If the functions in this loop block, the GUI will block
    while True:
        # Train / load pre-trained data

        # Create board representation from camera input
        board = get_board()

        board_svg, move = parse_board(board)
        if move is not None:
            board_img = svg_to_img(board_svg)
            my_gui.make_move(board_img, move)

        root.update_idletasks()
        root.update()

def main():
    # gui_thr = Thread(target=gui_loop)
    # gui_thr.start()
    # gui_thr.join()

    gui_loop()

if __name__ == "__main__":
    main()
