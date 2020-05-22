class Board:
    size = 8

    board = [[]]

    # Keeps track of the number of board on-board
    numWhite: int
    numBlack: int

    def __init__(self, board=None, num_black=12, num_white=12):
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)] if board is None else board
        self.numBlack = num_black
        self.numWhite = num_white
