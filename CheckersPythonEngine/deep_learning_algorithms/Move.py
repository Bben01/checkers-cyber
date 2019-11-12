from game_engine.Deplacement import Deplacement


class Move:
    def __init__(self, player_white, moved_on=None):
        self.player_white = player_white
        self.moved_on = moved_on

    def add_move(self, moved_on):
        """
        This method adds a move to the dict moves.
        :param moved_on: list of tuple that represent the positions that the piece went in
        :return: wether the list has been correctly added to the move
        """
        if self.moved_on is None:
            self.moved_on = moved_on
            return True
        else:
            return False

    def get_moves(self):
        return self.moved_on

    def get_killed_pieces(self):
        killed = []
        previous_move = None
        for move in self.moved_on:
            if previous_move is None:
                previous_move = move
            else:
                eaten_piece = Deplacement(previous_move[0], previous_move[1], move[0], move[1]).eaten_piece()
                if eaten_piece is not None:
                    killed.append(eaten_piece)
                previous_move = move

        return killed if killed is not [] else None

    def get_origin(self):
        return self.moved_on[0]

    def get_dest(self):
        return self.moved_on[-1]

    def __hash__(self):
        return hash((self.player_white, self.moved_on))
