class Plateau:
    taillePlateau = 8

    board = [[]]

    # Keeps track of the number of pieces on-board
    numWhite: int
    numBlack: int

    def __init__(self, board=None, num_black=0, num_white=0):
        self.board = [[None for _ in range(self.taillePlateau)] for _ in range(self.taillePlateau)] if board is None else board
        self.numBlack = num_black
        self.numWhite = num_white
