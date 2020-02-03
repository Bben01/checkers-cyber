from alpha_beta_pruning import EvaluateGenetics

ENNEMY_COLOR = True
One = True


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
        return EvaluateGenetics.evaluate(state, not ENNEMY_COLOR)
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
    if EvaluateGenetics.WEIGHTS is None:
        EvaluateGenetics.load_them(r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\genetic_algo\serialized")
    best_action = None
    best_value = float("-inf")
    for state_action in state.getPossibleActions():
        value = alphabeta(state.takeAction(state_action), 5, float("-inf"), float("inf"), True)
        if value > best_value:
            best_action = state_action
            best_value = value
    return best_action
