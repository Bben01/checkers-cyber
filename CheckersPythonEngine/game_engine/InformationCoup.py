from game_engine.Deplacement import Deplacement
from game_engine.Piece import Piece


class InformationCoup:
    errorMsg: str
    hasToEatAgain: bool
    endedTurn: bool
    posKilled: tuple
    pieceKilled: Piece
    isNewQueen: bool
    posNewQueen: tuple
    lastDeplacement: Deplacement

    def __init__(self, error_msg: str, has_to_eat_again: bool, ended_turn: bool, last_deplacement: Deplacement, piece_killed: Piece, pos_killed: tuple = None):  # NOQA
        self.errorMsg = error_msg
        self.hasToEatAgain = has_to_eat_again
        self.endedTurn = ended_turn
        self.posKilled = pos_killed
        self.pieceKilled = piece_killed
        self.isNewQueen = False
        self.lastDeplacement = last_deplacement

    @staticmethod
    def create_didnt_move():
        return InformationCoup("The piece didn't move!", False, False, None, None)

    @staticmethod
    def create_invalid_move(string: str):
        return InformationCoup(f"The move is invalid because { string }", False, False, None, None)

    @staticmethod
    def create_kill_move(pos_killed: tuple, has_to_eat_again: bool, last_deplacement: Deplacement, piece_killed: Piece):
        return InformationCoup("", has_to_eat_again, not has_to_eat_again, last_deplacement, piece_killed, pos_killed)

    @staticmethod
    def create_normal_move(last_deplacement: Deplacement):
        return InformationCoup("", False, True, last_deplacement, None)

    def add_new_queen(self, is_new_queen: bool, pos_new_queen: tuple):
        self.isNewQueen = is_new_queen
        self.posNewQueen = pos_new_queen
        return self
