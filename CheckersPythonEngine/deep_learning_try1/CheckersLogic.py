from deep_learning_algorithms import Helper
from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement
from game_engine.Piece import Piece


class Board:
    def __init__(self, taillePlateau=8):
        self.taillePlateau = taillePlateau
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

    def execute_move(self, move, color):
        origin = move.get_origin()
        destination = move.get_dest()
        is_new_queen = not self.pieces[origin[0]][origin[1]].isKing and \
                       ValidMoveMethods.check_new_queen(
                           Deplacement(origin[0], origin[1], destination[0], destination[1]), color)

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

