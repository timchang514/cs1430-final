from get_board import get_board
from render_board import *
from parse_board import *
from tkinter import Tk
from threading import Thread, Lock
from gui import *
import cv2
import numpy as np

def gui_loop():
    root = Tk()

    mt_board = svg_to_img(new_board())
    my_gui = ChessGUI(root, mt_board)

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(1)

    if vc.isOpened(): # try to get the first frame
        rval, board_img = vc.read()
    else:
        rval = False

    corners = None

    # Important: If the functions in this loop block, the GUI will block
    print("Locating board corners...")
    while rval:
        rval, board_img = vc.read()
        cv2.imshow("preview", board_img)

        # First run, get corners
        if corners is None:
            try:
                corners = find_corners(board_img)
                print("Corners found!")
            except Exception as e:
                print(e)
        else:
            squares = get_board_squares(np.array(board_img), corners)

            # Train / load pre-trained data
            pieces = None # predict(squares)

            # Create board representation from camera input
            board_pieces = get_board(pieces)

            board_svg, move = parse_board(board_pieces)
            if move is not None:
                board_png = svg_to_img(board_svg)
                my_gui.make_move(board_png, move)

        root.update_idletasks()
        root.update()

    cv2.destroyWindow("preview")

def main():
    # gui_thr = Thread(target=gui_loop)
    # gui_thr.start()
    # gui_thr.join()

    gui_loop()

    # cv2.namedWindow("preview")
    # vc = cv2.VideoCapture(1)
    #
    # if vc.isOpened(): # try to get the first frame
    #     rval, frame = vc.read()
    # else:
    #     rval = False
    #
    # # Important: If the functions in this loop block, the GUI will block
    # while rval:
    #     cv2.imshow("preview", frame)
    #     rval, frame = vc.read()
    #     key = cv2.waitKey(20)
    #     if key == 27: # exit on ESC
    #         break
    # cv2.destroyWindow("preview")

if __name__ == "__main__":
    main()
