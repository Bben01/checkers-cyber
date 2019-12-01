ENNEMY_IS_WHITE = True
KING_VALUE = 10
PIECE_VALUE = 2


def evaluate(state):
    if state.hasWon(False):
        return -120
    if state.hasWon(True):
        return 120
    util_value = 0
    for piece in state.plateau.board:
        if piece is not None:
            if piece.isKing:
                util_value += KING_VALUE if piece.isWhite == ENNEMY_IS_WHITE else -KING_VALUE
            else:
                util_value += PIECE_VALUE if piece.isWhite == ENNEMY_IS_WHITE else -PIECE_VALUE

    return util_value


def next_states(state):
    states = []
    for string_state in state.getPossibleActions():
        states.append(state.takeAction(string_state))

    return states


def alphabeta(state, depth, a, b, maximizingPlayer):
    if depth == 0 or state.isTerminal():
        return evaluate(state)
    if maximizingPlayer:
        value = float("-inf")
        for state_children in next_states(state):
            value = max(value, alphabeta(state_children, depth - 1, a, b, False))
            a = max(a, value)
            if a >= b:
                break
        return value
    else:
        value = float("inf")
        for state_children in next_states(state):
            value = min(value, alphabeta(state_children, depth - 1, a, b, True))
            b = min(b, value)
            if a >= b:
                break
        return value


def get_best_action(state):
    best_action = None
    best_value = float("-inf")
    for state_action in state.getPossibleActions():
        value = alphabeta(state.takeAction(state_action), 3, float("-inf"), float("inf"), True)
        if value > best_value:
            best_action = state_action
            best_value = value
    return best_action





