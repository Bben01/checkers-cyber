class Piece(object):
    isKing: bool
    isWhite: bool

    def __init__(self, white: bool, isKing: bool = False):
        self.isWhite = white
        self.isKing = isKing

    def __str__(self):
        return f"Piece(white={self.isWhite}, king={self.isKing})"

    def reverse_color(self):
        self.isWhite = not self.isWhite
