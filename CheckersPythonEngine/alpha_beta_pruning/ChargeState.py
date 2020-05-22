from copy import deepcopy

from deep_learning_algorithms.MctsMethods import State
from deep_learning_algorithms.Board import Board
from game_engine.Game import Game


def create_state(game_instance: Game):
    plateau = Board(board=deepcopy(game_instance.plateau.board), num_black=game_instance.plateau.numBlack,
                    num_white=game_instance.plateau.numWhite)
    state = State(plateau=plateau, is_white_turn=game_instance.plateau.isWhiteTurn)
    return state
