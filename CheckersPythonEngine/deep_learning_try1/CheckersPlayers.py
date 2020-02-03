import numpy as np
import requests

from MCTS import MCTS
from .engine import *


class RandomPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a

    def makeOpponentMove(self, move):
        pass

    def reset(self):
        pass


class NNetPlayer:
    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args
        # self.mcts = MCTS(game, nnet, args)
        # n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

    def play(self, board):
        # print("[",self.mcts.id,"] getActionProb:", self.mcts.numActionProbs+1) #, "took", time, "ms")
        return np.argmax(self.mcts.getActionProb(board, temp=0))

    def makeOpponentMove(self, move):
        pass

    def reset(self):
        self.mcts = MCTS(self.game, self.nnet, self.args)  # reset search tree
