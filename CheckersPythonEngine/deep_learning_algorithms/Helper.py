from deep_learning_algorithms.Move import Move
from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement


def calculate_recursive_eat_positions(board, x, y, has_to_eat=False):
    """
    Calculates all eat positions of a given piece on the board
    :param board: the board
    :param x: the x coordinate of the piece
    :param y: the y coordinate of the piece
    :param has_to_eat: whether the piece has to eat again or not
    :return: A dict of possible moves
    """
    count = 0
    moves = {}
    tmp = ValidMoveMethods.calculate_eat_positions(board, x, y, False, True, has_to_eat)
    if tmp is None:
        return None
    for _, move in tmp.items():
        other_paths = calculate_recursive_eat_positions(update_board(board, x, y, move), move[0], move[1], True)
        if other_paths is not None:
            for _, other in other_paths.items():
                moves[count] = [move].append(other)
                count += 1
        else:
            moves[count] = [move]
            count += 1
    return moves


def convert_to_list(dico, origin):
    """
    Convert {1: [( , ), ( , )], 2: ...} to [[( , ), ( , )], [...]]
    :param dico: the dict of moves {1: [( , ), ( , )], 2: ...}
    :param origin: a tuple that represents the origin (x, y)
    :return: [[( , ), ( , )], [...]]
    """
    moves_list = []
    for id_move, moves in dico.items():
        moves_list.append([origin].append(moves))
    return moves_list


def normalize_moves(moves, origin):
    """
    Convert {1: ( , ), 2: ...} to [[origin, ( , )], [...]]
    :param moves: dict of moves
    :param origin: a tuple that represents the origin (x, y)
    :return: [[origin, ( , )], [...]]
    """
    possible_moves = []
    if moves is None:
        return
    for _, move in moves.items():
        possible_moves.append([origin, move])
    return possible_moves


def update_board(board, x, y, move):
    board[move[0]][move[1]] = board[x][y]
    board[x][y] = None
    eaten = Deplacement(x, y, move[0], move[1]).eaten_piece()
    if eaten is not None:
        board[eaten[0]][eaten[1]] = None
    return board


def append_moves(original, to_append):
    if to_append is None:
        return
    for _, move in to_append.items():
        original[original["count"]] = move
        original["count"] += 1


def create_moves(list_of_moves, player_color):
    """
    Create [Move1([]), Move2([]), ...] from [[origin, ( , )], [...]]
    :param list_of_moves: the list of moves
    :param player_color: the color of the player
    :return: the created list
    """
    move_list = []
    if not list_of_moves:
        return
    for move in list_of_moves:
        move_list.append(Move(player_color, move))
        print(move)
    return move_list
