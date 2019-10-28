class Piece(object):
    isKing: bool
    isWhite: bool

    def __init__(self, white: bool):
        self.isWhite = white
        self.isKing = False
