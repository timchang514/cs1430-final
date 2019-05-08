from get_board import get_board
from render_board import *
from tkinter import Tk, Label, Button, Frame, Canvas, Listbox, Scrollbar
from PIL import Image, ImageTk
import cairosvg
import io
import time
from threading import Thread, Lock

class ChessGUI:
    def __init__(self, master, init_board):
        self.master = master
        master.title("Chess")
        master.geometry("600x400")

        self.board_label = Label(master, image=init_board)
        self.board_label.configure(image=init_board)
        self.board_label.image = init_board
        self.board_label.grid(row=0, column=0, rowspan = 20)

        self.newGameButton = Button(master, text='New Game', command=self.newGame)
        self.newGameButton.grid(row=0, column=1)

        self.saveGameButton = Button(master, text='Save Game', command=self.saveGame)
        self.saveGameButton.grid(row=0, column=2)

        self.moves_frame = Frame(master, width=30, height=24)
        self.moves_frame.grid(row=1, column=1, columnspan=2)

        self.moves = Listbox(self.moves_frame, width=30, height=24, font=("Helvetica", 12))
        self.moves.grid(row=0, column=0)

    def newGame(self):
        print("New Game")

    def saveGame(self):
        print("Save Game")

    def make_move(self, board, move):
        self.set_board(board)
        self.moves.insert("end", move)

    def set_board(self, board):
        self.board = board
        self.board_label.configure(image=board)
        self.board_label.image = board

def flattenAlpha(img):
    alpha = img.split()[-1]  # Pull off the alpha layer
    ab = alpha.tobytes()  # Original 8-bit alpha

    checked = []  # Create a new array to store the cleaned up alpha layer bytes

    # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
    transparent = 50  # change to suit your tolerance for what is and is not transparent

    p = 0
    for pixel in range(0, len(ab)):
        if ab[pixel] < transparent:
            checked.append(0)  # Transparent
        else:
            checked.append(255)  # Opaque
        p += 1

    mask = Image.frombytes('L', img.size, bytes(checked))

    img.putalpha(mask)

    return img

def svg_to_img(svg):
    bytes = cairosvg.svg2png(svg)
    image = Image.open(io.BytesIO(bytes))
    image_tk = ImageTk.PhotoImage(image=flattenAlpha(image))
    return image_tk
