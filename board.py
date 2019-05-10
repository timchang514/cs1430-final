from enum import Enum

class PieceName(Enum):
    EMPTY = 1
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5
    PAWN = 6

class Player(Enum):
    WHITE = 1
    BLACK = 2

class PPiece:
    # Type is a PieceName
    # Player is a player
    # position is a tuple ([1-8], [1-8]) of their position on the board.
    # q: Should bottom left of the board be 0,0, or top left?

    # def __init__(self, type, player, position):
    #     self.type = type
    #     self.player = player
    #     self.position = position

    # Piece should be a chess.Piece
    def __init__(self, piece, position):
        self.piece = piece
        self.position = position
