from game_engine import Controller
from game_engine.MoveInfos import MoveInfos
from game_engine.Plateau import Plateau


class Game:
    plateau: Plateau

    hasToPlayAgain: bool = False
    posPieceToPlay: ()

    def __init__(self, board=None, hasToPlayAgain=False):
        self.plateau = Plateau() if board is None else board
        self.hasToPlayAgain = hasToPlayAgain
        self.posPieceToPlay = ()

    def check_victory(self, ennemy_color: bool):
        # Just for now
        if not self.plateau.has_pieces_left(ennemy_color):
            return True
        if Controller.possible_plays(self, not ennemy_color, False) is None:
            return True
        return False

    def end_turn(self):
        self.plateau.end_turn()
        self.hasToPlayAgain = False

    def analize_info(self, infos: MoveInfos):
        return_message = ""
        separator = "-"
        is_false = "0" + separator
        # There was an error
        if infos.errorMsg != "":
            return "1" + separator + ("1" if not self.hasToPlayAgain else "0") + infos.errorMsg + separator + "0" \
                   + separator + "0" + separator + "0" + separator + "0" + separator + "0"
        else:
            return_message += is_false
        # There is a new Queen
        if infos.isNewQueen:
            return_message += "1" + repr(infos.posNewQueen[0]) + repr(infos.posNewQueen[1]) + separator
            self.plateau.board[infos.posNewQueen[0]][infos.posNewQueen[1]].isKing = True
        else:
            return_message += is_false
        if infos.posKilled is not None:
            return_message += "1" + repr(infos.posKilled[0]) + repr(infos.posKilled[1])
            if infos.hasToEatAgain:
                return_message += "1"
                self.hasToPlayAgain = True
                self.posPieceToPlay = (infos.posKilled[0], infos.posKilled[1])
            else:
                return_message += "0"
            return_message += separator
        else:
            return_message += is_false
        # Ended turn
        if infos.endedTurn:
            return_message += "1" + separator
            self.end_turn()
        else:
            return_message += is_false
        return_message += "1" + repr(infos.lastMove.destination[0]) + repr(infos.lastMove.destination[1])
        # Victory
        if self.check_victory(self.plateau.isWhiteTurn):
            return_message += separator + "1" + ("Black won!" if self.plateau.isWhiteTurn else "White won!")
        else:
            return_message += separator + "0"
        return_message += separator + f"1{infos.lastMove.origin[0]}{infos.lastMove.origin[1]}"
        return return_message
