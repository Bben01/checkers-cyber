import game_engine.ValidMoveMethods as Helper
from alpha_beta_pruning import param

"""
This will be used to change the weights of every info on the board according to a genetic algorithm
The array of values will be this: [nb_of_pawn, nb_of_king, nb_safe_pawn, nb_safe_king, nb_moveable_pawn, nb_moveable_king, distance_prom_line, nb_unoccupied_prom_line]
Special patterns could be added after
"""


def number_moveable(state, color):
    """
    Gets the number of moveable pawns and kings for the player
    :param state: the current state of the game
    :param color: the player to check
    :return: the number of moveable pawns and kings in form of a tuple (pawn, king)
    """
    size = state.plateau.taillePlateau
    pawn = 0
    king = 0
    for i in range(size):
        for j in range(i % 2, size, 2):
            piece = state.plateau.board[i][j]
            if piece is not None:
                if piece.isWhite == color:
                    positions_dict = Helper.calculate_eat_positions(state.plateau.board, i, j, True, True, False)
                    if positions_dict is not None:
                        if piece.isKing:
                            king += 1
                        else:
                            pawn += 1

    return pawn, king


def number_safe(state, color):
    size = state.plateau.taillePlateau
    pawn = 0
    king = 0
    for i in range(size):
        for j in range(i % 2, size, 2):
            piece = state.plateau.board[i][j]
            if piece is not None and piece.isWhite == color:
                if i == 0 or j == 0 or i == size - 1 or j == size - 1:
                    if piece.isKing:
                        king += 1
                    else:
                        pawn += 1

    return pawn, king


def number_pieces(state, color):
    pawn = 0
    king = 0
    for row in state.plateau.board:
        for piece in row:
            if piece is not None and piece.isWhite == color:
                if piece.isKing:
                    king += 1
                else:
                    pawn += 1

    return pawn, king


def prom_line(state, color):
    """
    Compute the aggregated distance to prom line and the number of occupied spot in prom line
    :param state: current state of the game
    :param color: the player to check
    :return: a tuple (distance, unoccupied_field)
    """
    size = state.plateau.taillePlateau
    if color:
        prom_line_number = size - 1
    else:
        prom_line_number = 0
    distance_sum = 0
    occupied = 0
    for i in range(size):
        for j in range(i % 2, size, 2):
            piece = state.plateau.board[i][j]
            if piece is None or piece.isKing:
                continue
            if piece.isWhite == color:
                distance_sum += abs(prom_line_number - j)
            if piece.isWhite != color and j == size - prom_line_number - 1:
                occupied += 1

    return distance_sum, size / 2 - occupied


def evaluate(state, color):
    ally, enemy = get_weight(state, color)
    computed_sum = 0
    for i in range(len(ally) - 1):
        computed_sum += param.WEIGHTS[0][i][0] * ally[i] + param.WEIGHTS[0][i][1]
        computed_sum += param.WEIGHTS[1][i][0] * ally[i] + param.WEIGHTS[1][i][1]

    return computed_sum


def get_weight(state, color):
    """
    The array of values will be this: [nb_of_pawn, nb_of_king, nb_safe_pawn, nb_safe_king, nb_moveable_pawn,
                                       nb_moveable_king, distance_prom_line, nb_unoccupied_prom_line]
    Everything in double: one for the player's color, and one for the opponent's
    :param state: current state of the game
    :param color: True for white player, False for black
    :return: the arrays of info, in form of a tuple
    """
    ally_array = list()
    enemy_array = list()
    ally_array.extend(number_pieces(state, color))
    enemy_array.extend(number_pieces(state, not color))

    ally_array.extend(number_safe(state, color))
    enemy_array.extend(number_safe(state, not color))

    ally_array.extend(number_moveable(state, color))
    enemy_array.extend(number_moveable(state, not color))

    ally_array.extend(prom_line(state, color))
    enemy_array.extend(prom_line(state, not color))

    return ally_array, enemy_array
