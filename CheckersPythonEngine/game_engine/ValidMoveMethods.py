from game_engine.Deplacement import Deplacement
from game_engine.InformationValidation import InformationValidation
from game_engine.Plateau import Plateau


def valid_move(board: [], d: Deplacement, has_to_eat_again: bool):
    if d.null_move():
        return InformationValidation.create_not_move()

    # Pas dans le plateau
    if Plateau.out_of_bounds(d.destination[0], d.destination[1]):
        return InformationValidation.create_wrong_move("the target zone is outside the board.")

    if Plateau.occupied(board, d.destination[0], d.destination[1]):
        return InformationValidation.create_wrong_move("the target zone is occupied.")

    selected = board[d.origin[0]][d.origin[1]]
    has_to_kill = calculate_eat_positions(board, d.origin[0], d.origin[1], False, True, has_to_eat_again)

    has_something_to_eat_var = has_something_to_eat(board, selected.isWhite, has_to_eat_again)
    is_killing_again_var = is_killing_again(has_to_kill, d.destination[0],
                                            d.destination[1]) if has_something_to_eat_var else False

    # The player has to kill and is actually killing a piece
    if has_something_to_eat_var and is_killing_again_var:
        v = d.eaten_piece()
        return InformationValidation.create_kill_move((v[0], v[1]))
    elif has_something_to_eat_var and not is_killing_again_var:
        return InformationValidation.create_wrong_move("you are forced to eat a piece.")

    if selected is not None:
        # Didnt move
        if d.null_move():
            return InformationValidation.create_not_move()
        # Invalid move
        if not valid_rules(board, d):
            return InformationValidation.create_wrong_move("the rules are not respected.")
        # Normal move
        return InformationValidation.create_normal_move()

    return InformationValidation.create_wrong_move("something went wrong...")


def is_killing_again(has_to_kill, x, y):
    """
    If the piece can eat, it has to eat, and this method checks if it is actually eating
    :param has_to_kill: a dictionnary of tuples
    :param x: an integer
    :param y: an integer
    :return: checks if the player is actually eating
    """
    if has_to_kill is None:
        return False
    for _, pair in has_to_kill.items():
        if pair[0] == x and pair[1] == y:
            return True

    return False


def valid_rules(board: [[]], d: Deplacement):
    x1 = d.origin[0]
    x2 = d.destination[0]
    y1 = d.origin[1]
    y2 = d.destination[1]

    return move(board, True, x1, y1, x2, y2) or move(board, False, x1, y1, x2, y2)


def move(board: [[]], check_white: bool, x1, y1, x2, y2):
    delta_move_x = abs(x1 - x2)
    delta_move_y = y2 - y1
    is_white = board[x1][y1].isWhite
    is_king = board[x1][y1].isKing

    multiplier = 1 if check_white else -1

    if is_white and check_white or not is_white and not check_white or is_king:
        if delta_move_x == 1 and delta_move_y == multiplier:
            return True

    return False


def has_something_to_eat(board: [[]], is_white: bool, has_to_eat_again: bool):
    for i in range(len(board)):
        for j in range(len(board)):
            p = board[i][j]
            if p is not None and p.isWhite == is_white and calculate_eat_positions(board, i, j, False, True,
                                                                                   has_to_eat_again) is not None:
                return True

    return False


def calculate_eat_positions(board: [[]], x, y, check_normal: bool, check_kill_positions: bool, has_to_eat_again: bool):
    positions = {}
    v_piece = (x, y)
    vectors = [
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    empty_dict = True
    count_positive = 1
    count_negative = -1

    for vector in vectors:
        if check_kill_positions and check(board, v_piece, vector) and (has_to_eat_again or can_move_direction(board, x, y, vector)):
            positions[count_positive] = (v_piece[0] + vector[0] * 2, v_piece[1] + vector[1] * 2)
            empty_dict = False
            count_positive += 1
            print(f"Le pion peut manger: {concat_int_int_tuples(vector, v_piece)}")

        ok = check_normal and (not Plateau.out_of_bounds(v_piece[0] + vector[0], v_piece[1] + vector[1])) and \
             board[v_piece[0] + vector[0]][v_piece[1] + vector[1]] is None
        if ok and can_move_direction(board, x, y, vector):
            positions[count_negative] = concat_int_int_tuples(v_piece, vector)
            empty_dict = False
            count_negative -= 1
            print(f"Le pion peut se deplacer sur la case: {concat_int_int_tuples(v_piece, vector)}")

    return positions if not empty_dict else None


def can_move_direction(board: [[]], x, y, direction: ()):
    p = board[x][y]
    if p.isKing:
        return True
    if p.isWhite:
        return direction == (-1, 1) or direction == (1, 1)

    return direction == (-1, -1) or direction == (1, -1)


def check(board: [[]], v: (), direction: ()):
    range_x = v[0] + direction[0] * 2
    range_y = v[1] + direction[1] * 2

    if Plateau.out_of_bounds(range_x, range_y) or board[v[0] + direction[0]][v[1] + direction[1]] is None:
        return False

    different_color = board[v[0] + direction[0]][v[1] + direction[1]].isWhite != board[v[0]][v[1]].isWhite
    unnocupied_target = board[range_x][range_y] is None

    return different_color and unnocupied_target


def check_new_queen(d: Deplacement, check_white: bool):
    zone_dames = Plateau.taillePlateau - 1 if check_white else 0
    if d.destination[1] == zone_dames:
        return True
    return False


def pos_new_queen(is_new_queen: bool, d: Deplacement):
    return (d.destination[0], d.destination[1]) if is_new_queen else None


def concat_int_int_tuples(first_tuple: (int, int), secont_tuple: (int, int)):
    return first_tuple[0] + secont_tuple[0], first_tuple[1] + secont_tuple[1]
