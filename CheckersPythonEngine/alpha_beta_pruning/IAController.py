from alpha_beta_pruning import ChargeState, Alphabeta


def controller(game_state):
    """
    Take a Game State from the Controller of the game_engine package and
    returns an action
    :param game_state: the current game_state
    :return: the action to take
    """
    state = ChargeState.create_state(game_state)
    best_state = Alphabeta.get_best_action(state)
    return best_state


def list_actions(best_move):
    list_moves = []
    previous_move = None
    for current_move in best_move.get_moves():
        if previous_move is None:
            previous_move = current_move
            continue
        list_moves.append((previous_move, current_move))
        previous_move = current_move

    return list_moves
