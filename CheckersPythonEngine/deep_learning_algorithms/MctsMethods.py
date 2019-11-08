import copy

from deep_learning_algorithms import Helper
from deep_learning_algorithms.InfosOnMoves import KillMoves
from deep_learning_algorithms.Plateau import Plateau
from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement
from game_engine.Piece import Piece


class State:
    plateau: Plateau
    killMoves: KillMoves

    isWhiteTurn: bool

    def __init__(self, is_white_turn=True, plateau=Plateau(), kill_moves=KillMoves()):
        self.isWhiteTurn = is_white_turn
        self.plateau = plateau
        self.killMoves = kill_moves

    @staticmethod
    def initial_state():
        plateau = Plateau()
        for y in range(int(Plateau.taillePlateau - 1 / 2)):
            odd_row = y % 2 == 0
            for x in range(Plateau.taillePlateau, step=2):
                if odd_row:
                    plateau.board[x][y] = Piece(True)

        for y in range(start=Plateau.taillePlateau - 1, stop=int(Plateau.taillePlateau - 1 / 2) + 1, step=-1):
            odd_row = y % 2 == 0
            for x in range(Plateau.taillePlateau, step=2):
                if odd_row:
                    plateau.board[x][y] = Piece(False)

        return State(is_white_turn=True, plateau=plateau)

    def make_new_game_state(self, move_id, new_queen):
        moves = self.killMoves.get_move(move_id)
        previous = None
        new_state = copy.deepcopy(self.plateau.board)
        for tup in moves:
            if previous is None:
                previous = tup
            else:
                new_state = Helper.update_board(new_state, previous[0], previous[1], tup)
        if new_queen:
            new_state.plateau.board[moves[-1][0]][moves[-1][1]].isKing = True
        new_state.isWhiteTurn = not self.isWhiteTurn
        for _ in self.killMoves.get_killed_pieces(move_id):
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
        has_to_eat_something = self.has_to_eat()
        plays = {}
        for x in range(self.plateau.taillePlateau):
            for y in range(self.plateau.taillePlateau):
                current_piece = self.plateau.board[x][y]
                if current_piece is not None and current_piece.isWhite == self.isWhiteTurn:
                    if has_to_eat_something:
                        tmp = Helper.calculate_recursive_eat_positions(self.plateau.board, x, y)
                    else:
                        tmp = Helper.normalize_moves(
                            ValidMoveMethods.calculate_eat_positions(self.plateau.board, x, y, True, False, False))
                    Helper.append_moves(plays, tmp)
        del plays["count"]
        if has_to_eat_something:
            self.killMoves.add_moves(plays)
        return plays

    def takeAction(self, action):
        # Only one time
        move_id = 0
        for id_number, first_action in action.items():
            move_id = id_number
            action = first_action
            break
        origin = action[0]
        destination = action[1]
        is_new_queen = not self.plateau.board[origin[0]][origin[1]].isKing and \
                       ValidMoveMethods.check_new_queen(
                           Deplacement(origin[0], origin[1], destination[0], destination[1]), self.isWhiteTurn)
        # Killed
        if self.killMoves.get_killed_pieces(move_id) is not None:
            return self.make_new_game_state(move_id, is_new_queen)
        # Normal move
        else:
            return self.make_new_game_state(move_id, is_new_queen)

    def isTerminal(self):
        return not self.has_something_to_play(check_other=True) or self.has_won(True) or self.has_won(False)

    def getReward(self):
        if self.isWhiteTurn and self.has_won(True):
            return 1
        if not self.isWhiteTurn and self.has_won(False):
            return 1
        return 0
