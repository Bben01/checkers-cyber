from __future__ import print_function

import copy
import sys

from deep_learning_try1.CheckersLogic import Board

sys.path.append('..')
from deep_learning_try1.Game import Game
from deep_learning_algorithms.Plateau import Plateau
import numpy as np


class CheckersGame(Game):
    def __init__(self, taillePlateau):
        super().__init__()
        self.taillePlateau = taillePlateau

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        b = Board(self.taillePlateau)
        return np.array(b.pieces)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return self.taillePlateau, self.taillePlateau

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return self.taillePlateau * self.taillePlateau + 1

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or 0)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        b = Board(self.taillePlateau)
        b.pieces = copy.deepcopy(board)
        b.execute_move(action, self._playerToBool(player))
        return b.pieces, -player

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        b = Board(self.taillePlateau)
        b.pieces = copy.deepcopy(board)
        legal_moves = b.get_legal_moves(self._playerToBool(player))
        return legal_moves

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or 0)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        # TODO: voir comment faire puisqu'eux le font avec des 1 au niveau des cases possibles a jouer
        b = Board(self.taillePlateau)
        b.pieces = copy.deepcopy(board)
        num = player if b.countPieces(self._playerToBool(player)) == 0 else 0 if b.countPieces(self._playerToBool(-player)) else -player
        return num

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or 0)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        # If white
        if self._playerToBool(player):
            return board
        # If black
        for row in board:
            for piece in row:
                if piece is not None:
                    piece.reverse_color()

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass

    @staticmethod
    def _playerToBool(player):
        return True if player == 1 else False
