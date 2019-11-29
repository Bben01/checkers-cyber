from copy import deepcopy

from deep_learning_algorithms.MctsMethods import State
from deep_learning_algorithms.Plateau import Plateau
from game_engine.Jeu import Jeu


def create_state(game_instance: Jeu):
    plateau = Plateau(board=deepcopy(game_instance.plateau.pieces), num_black=game_instance.plateau.numBlack,
                      num_white=game_instance.plateau.numWhite)
    state = State(plateau=plateau, is_white_turn=game_instance.plateau.isWhiteTurn)
    return state
