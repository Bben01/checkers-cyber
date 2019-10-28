from game_engine.Deplacement import Deplacement
from game_engine.InformationCoup import InformationCoup
from game_engine.Plateau import Plateau

dictionnaire = {"false": False, "true": True}


class Jeu:
    plateau: Plateau

    hasToPlayAgain: bool = False
    posPieceToPlay: ()

    def __init__(self):
        self.plateau = Plateau()
        self.hasToPlayAgain = False
        self.posPieceToPlay = ()

    def check_victory(self, check_white: bool):
        # TODO: a implementer
        # Just for now
        if not self.plateau.has_pieces_left(not check_white):
            return True
        return False

    def end_turn(self, last_deplacement: Deplacement):
        # TODO: Call here for the endTurn in the graphic interface
        victory = self.check_victory(self.plateau.isWhiteTurn)
        self.plateau.end_turn(last_deplacement)
        self.hasToPlayAgain = False
        if victory:
            # TODO: animate victory
            pass

    def analize_info(self, infos: InformationCoup):
        return_message = ""
        separator = "-"
        is_false = "0" + separator
        # There was an error
        if infos.errorMsg != "":
            return "1" + separator + ("1" if not self.hasToPlayAgain else "0") + infos.errorMsg + separator + "0" + separator + "0" + separator + "0"
        else:
            return_message += is_false
        # There is a new Queen
        if infos.isNewQueen:
            return_message += "1" + repr(infos.posNewQueen[0]) + repr(infos.posNewQueen[1]) + separator
            self.plateau.pieces[infos.posNewQueen[0]][infos.posNewQueen[1]].isKing = True
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
            self.end_turn(infos.lastDeplacement)
        else:
            return_message += is_false
        return return_message + "1" + repr(infos.lastDeplacement.destination[0]) + repr(
            infos.lastDeplacement.destination[1])
