import chess
import chess.svg

def parse_board(board):
    # TODO: Parse board data into board object

    return new_board(), None

def empty_board():
    board = chess.Board("8/8/8/8/8/8/8/8")
    board_svg = chess.svg.board(board=board)
    return board_svg

def new_board():
    board = chess.Board()
    board_svg = chess.svg.board(board=board)
    return board_svg

def random_board():
    board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
    board_svg = chess.svg.board(board=board)
    return board_svg, "test"
