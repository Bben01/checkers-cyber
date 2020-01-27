import game_engine.ValidMoveMethods as Helper

ENNEMY_COLOR = True
WIN = float("inf")
LOSS = float("-inf")
KING_VALUE = 15
PIECE_VALUE = 7


"""
This will be used to change the weights of every info on the board according to a genetic algorithm
The array of values will be this: [nb_of_pawn, nb_of_king, nb_safe_pawn, nb_safe_king, nb_moveable_pawn, nb_moveable_king, distance_prom_line, nb_unoccupied_prom_line]
Special patterns could be added after
"""


def get_number_moves(state, player_color):
    """
    Gets the number of possible moves for the player
    :param state: the current state of the game
    :param player_color: the player to chack
    :return: the number of possible moves in form of a tuple (normals, eat_moves)
    """
    size = state.plateau.taillePlateau
    count_normals = 0
    count_eats = 0
    for i in range(size):
        for j in range(i % 2, size, 2):
            piece = state.plateau.board[i][j]
            if piece is not None:
                if piece.isWhite == player_color:
                    positions_dict = Helper.calculate_eat_positions(state.plateau.board, i, j, True, True, False)
                    for key, value in positions_dict.items():
                        if key < 0:
                            count_eats += 1
                        else:
                            count_normals += 1

    return count_normals, count_eats


def number_pieces(state):
    util_value = 0
    for row in state.plateau.board:
        for piece in row:
            if piece is not None:
                if piece.isKing:
                    util_value += KING_VALUE if piece.isWhite != ENNEMY_COLOR else -KING_VALUE
                else:
                    util_value += PIECE_VALUE if piece.isWhite != ENNEMY_COLOR else -PIECE_VALUE

    return util_value


def evaluate(state):
    self_count_normal, self_count_eat = get_number_moves(state, not ENNEMY_COLOR)
    enemy_count_normal, enemy_count_eat = get_number_moves(state, ENNEMY_COLOR)


def get_weight(state, color):
    """
    The array of values will be this: [nb_of_pawn, nb_of_king, nb_safe_pawn, nb_safe_king, nb_moveable_pawn,
                                       nb_moveable_king, distance_prom_line, nb_unoccupied_prom_line]
    :param state: current state of the game
    :param color: True for white player, False for black
    :return: the array of info
    """
    pass
