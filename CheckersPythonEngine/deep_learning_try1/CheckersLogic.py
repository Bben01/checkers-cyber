from deep_learning_algorithms import Helper
from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement
from game_engine.Piece import Piece


class Board:
    def __init__(self, taille_plateau=8):
        self.taillePlateau = taille_plateau
        self.pieces = [[None for _ in range(self.taillePlateau)] for _ in range(self.taillePlateau)]

        for y in range(int(self.taillePlateau - 1 / 2)):
            odd_row = y % 2 == 0
            for x in range(self.taillePlateau, step=2):
                if odd_row:
                    self.pieces[x][y] = Piece(True)

        for y in range(start=self.taillePlateau - 1, stop=int(self.taillePlateau - 1 / 2) + 1, step=-1):
            odd_row = y % 2 == 0
            for x in range(self.taillePlateau, step=2):
                if odd_row:
                    self.pieces[x][y] = Piece(False)

        # TODO: faire quelque chose pour cloner le plateau?

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def countPieces(self, color):
        """
        color = True > white
        color = False > black
        """
        count = 0
        for row in self.pieces:
            for piece in row:
                if piece is not None:
                    if piece.isWhite() == color:
                        count += 1

        return count

    def get_legal_moves(self, color):
        has_to_eat_something = self.has_to_eat(color)
        plays = []
        for x in range(self.taillePlateau):
            for y in range(self.taillePlateau):
                current_piece = self.pieces[x][y]
                if current_piece is not None and current_piece.isWhite == color:
                    if has_to_eat_something:
                        tmp = Helper.add_origin(Helper.calculate_recursive_eat_positions(self.pieces, x, y),
                                                (x, y))
                    else:
                        tmp = Helper.normalize_moves(
                            ValidMoveMethods.calculate_eat_positions(self.pieces, x, y, True, False, False),
                            (x, y))
                    if tmp is not None:
                        plays.extend(Helper.create_moves(tmp, color))
        return plays

    def has_to_eat(self, color):
        return ValidMoveMethods.has_something_to_eat(self.pieces, color, False)

    def has_legal_moves(self, color):
        for x in range(self.taillePlateau):
            for y in range(self.taillePlateau):
                current_piece = self.pieces[x][y]
                if current_piece is not None and current_piece.isWhite == color and \
                        ValidMoveMethods.calculate_eat_positions(self.pieces, x, y, True, True, False) is not None:
                    return True
        return False

    @staticmethod
    def get_action_size():
        # the method supports n=8 only
        # assert self.n == 8
        # action space
        # square_from = self.n*self.n/2 = 8x8/2 = 32 (for n=8, 5 bits)
        # move vector, max of 7 squares in 4 directions = (self.n-1)*4 = 7*4 = 28 (for n=8)
        # maxNumberOfMoves = 32*28 = 896
        # to simplify action encoding/decoding take max as bin(28)_bin(32) = 11100_11111 = 927
        return 927

    def execute_move(self, move, color):
        origin = move.get_origin()
        destination = move.get_dest()
        is_new_queen = not self.pieces[origin[0]][origin[1]].isKing and ValidMoveMethods.check_new_queen(Deplacement(
            origin[0], origin[1], destination[0], destination[1]), color)

        moves = move.get_moves()
        previous = None
        for tup in moves:
            if previous is None:
                previous = tup
            else:
                self.pieces = Helper.update_board(self.pieces, previous[0], previous[1], tup)
                previous = tup
        if is_new_queen:
            self.pieces[moves[-1][0]][moves[-1][1]].isKing = True

    def get_game_result(self, color):
        """ Check whether the game is over (previous method name was is_win() ).
            Check whether the given player has captured all opponent's pieces
            or given player's pieces have valid moves
        @param color (1=white,-1=black) - player to move
        @return: 1: if the given player won, -1: if the given player lost, 0: if game continues
        """
        pass

    def display(self):
        pass
