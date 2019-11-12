from deep_learning_algorithms.Move import Move
from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement


def calculate_recursive_eat_positions(board, x, y, has_to_eat=False):
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


def convert_to_list(dico):
    moves_list = []
    for id_move, moves in dico.items():
        moves_list.append(tuple(moves))
    return moves_list


def update_board(board, x, y, move):
    board[move[0]][move[1]] = board[x][y]
    board[x][y] = None
    eaten = Deplacement(x, y, move[0], move[1]).eaten_piece()
    if eaten is not None:
        board[eaten[0]][eaten[1]] = None
    return board


def normalize_moves(moves):
    possible_moves = []
    for _, move in moves.items():
        possible_moves.append(move)
    return possible_moves


def append_moves(original, to_append):
    if to_append is None:
        return
    for _, move in to_append.items():
        original[original["count"]] = move
        original["count"] += 1


def create_moves(list_of_moves, player_color):
    move_list = []
    for move in list_of_moves:
        move_list.append(Move(player_color, move))
    return move_list
