import copy

from deep_learning_algorithms import Helper
from deep_learning_algorithms.Move import Move
from deep_learning_algorithms.Plateau import Plateau
from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement
from game_engine.Piece import Piece


class State:
    plateau: Plateau

    isWhiteTurn: bool

    def __init__(self, is_white_turn=True, plateau=Plateau()):
        self.isWhiteTurn = is_white_turn
        self.plateau = plateau

    @staticmethod
    def initial_state():
        plateau = Plateau()
        for y in range(int(Plateau.taillePlateau - 1 / 2)):
            odd_row = y % 2 == 0
            for x in range(0, Plateau.taillePlateau, 2):
                if odd_row:
                    plateau.board[x][y] = Piece(True)

        for y in range(Plateau.taillePlateau - 1, int(Plateau.taillePlateau - 1 / 2) + 1, -1):
            odd_row = y % 2 == 0
            for x in range(Plateau.taillePlateau, step=2):
                if odd_row:
                    plateau.board[x][y] = Piece(False)

        return State(is_white_turn=True, plateau=plateau)

    def make_new_game_state(self, move: Move, new_queen):
        moves = move.get_moves()
        previous = None
        new_state = State(not self.isWhiteTurn, copy.deepcopy(self.plateau))
        for tup in moves:
            if previous is None:
                previous = tup
            else:
                new_state.plateau.board = Helper.update_board(new_state.plateau.board, previous[0], previous[1], tup)
                previous = tup
        if new_queen:
            new_state.plateau.board[moves[-1][0]][moves[-1][1]].isKing = True
        new_state.isWhiteTurn = not self.isWhiteTurn
        for _ in move.get_killed_pieces():
            new_state.plateau.numWhite -= 0 if self.isWhiteTurn else 1
            new_state.plateau.numBlack -= 1 if self.isWhiteTurn else 0
        if not new_state.has_something_to_play():
            new_state.isWhiteTurn = not new_state.isWhiteTurn
        return new_state

    def has_to_eat(self):
        return ValidMoveMethods.has_something_to_eat(self.plateau.board, self.isWhiteTurn, False)

    def has_something_to_play(self, check_other=False):
        for x in range(self.plateau.taillePlateau):
            for y in range(self.plateau.taillePlateau):
                current_piece = self.plateau.board[x][y]
                if current_piece is not None and (check_other or current_piece.isWhite == self.isWhiteTurn) and \
                        ValidMoveMethods.calculate_eat_positions(self.plateau.board, x, y, True, True,
                                                                 False) is not None:
                    return True
        return False

    def has_won(self, check_white):
        if check_white:
            return self.plateau.numBlack == 0
        else:
            return self.plateau.numWhite == 0

    def getPossibleActions(self):
        """
        Return all possible actions (legal ones) from the current state
        :return: a list of Move
        """
        has_to_eat_something = self.has_to_eat()
        plays = []
        for x in range(self.plateau.taillePlateau):
            for y in range(self.plateau.taillePlateau):
                current_piece = self.plateau.board[x][y]
                if current_piece is not None and current_piece.isWhite == self.isWhiteTurn:
                    if has_to_eat_something:
                        tmp = Helper.add_origin(Helper.calculate_recursive_eat_positions(self.plateau.board, x, y), (x, y))
                    else:
                        tmp = Helper.normalize_moves(
                            ValidMoveMethods.calculate_eat_positions(self.plateau.board, x, y, True, False, False), (x, y))
                    if tmp is not None:
                        plays.extend(Helper.create_moves(tmp, self.isWhiteTurn))
        return plays

    def takeAction(self, move):
        origin = move.get_origin()
        destination = move.get_dest()
        is_new_queen = not self.plateau.board[origin[0]][origin[1]].isKing and \
                       ValidMoveMethods.check_new_queen(
                           Deplacement(origin[0], origin[1], destination[0], destination[1]), self.isWhiteTurn)

        return self.make_new_game_state(move, is_new_queen)

    def isTerminal(self):
        return not self.has_something_to_play(check_other=True) or self.has_won(True) or self.has_won(False)

    def getReward(self):
        if self.isWhiteTurn and self.has_won(True):
            return 1
        if not self.isWhiteTurn and self.has_won(False):
            return -1
        return 0

    @staticmethod
    def print_board(board):
        string = ""
        for k, i in enumerate(board):
            for j in board[k]:
                string += '{:^30}'.format(str(j))
            string += "\n"
        return string
