from game_engine.Deplacement import Deplacement


class KillMoves:
    moves = {}

    def __init__(self):
        self.moves = {}

    def add_move(self, id_number, moved_on: []):
        """
        This method adds a move to the dict moves.
        :param id_number: the id of the move
        :param moved_on: list of tuple that represent the positions that the piece went in
        :return: wether the piece has been correctly added to the dict or not, for example if the id is already in the dict
        """
        if self.moves[id_number] is None:
            self.moves[id_number] = moved_on
            return True
        else:
            return False

    def add_moves(self, moves):
        for id_move, move in moves.items():
            self.add_move(id_move, move)

    def get_move(self, id_number):
        return self.moves[id_number]

    def get_killed_pieces(self, id_number):
        killed = []
        previous_move = None
        for move in self.moves[id_number]:
            if previous_move is None:
                previous_move = move
            else:
                eaten_piece = Deplacement(previous_move[0], previous_move[1], move[0], move[1]).eaten_piece()
                if eaten_piece is not None:
                    killed.append(eaten_piece)
                previous_move = move

        return killed if killed is not [] else None
