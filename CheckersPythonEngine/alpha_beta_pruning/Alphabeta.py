ENNEMY_IS_WHITE = True
KING_VALUE = 15
PIECE_VALUE = 7
One = True


def evaluate(state):
    if state.has_won(False):
        return -120
    if state.has_won(True):
        return 120
    util_value = 0
    for row in state.plateau.board:
        for piece in row:
            if piece is not None:
                if piece.isKing:
                    util_value += -KING_VALUE if piece.isWhite == ENNEMY_IS_WHITE else KING_VALUE
                else:
                    util_value += -PIECE_VALUE if piece.isWhite == ENNEMY_IS_WHITE else PIECE_VALUE

    return util_value


def next_states(state):
    global One
    states = []
    for string_state in state.getPossibleActions():
        states.append(state.takeAction(string_state))
        if One:
            print(states[0].print_board(states[0].plateau.board))
            One = False

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
        value = alphabeta(state.takeAction(state_action), 5, float("-inf"), float("inf"), True)
        print(f'value={value}, best_value={best_value}')
        if value > best_value:
            best_action = state_action
            best_value = value
    return best_action
