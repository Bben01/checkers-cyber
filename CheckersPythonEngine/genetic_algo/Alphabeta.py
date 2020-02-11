from genetic_algo import EvaluateGenetics
from genetic_algo.args import args

ENNEMY_COLOR = False
One = True


def change_player(color=not ENNEMY_COLOR):
    global ENNEMY_COLOR
    ENNEMY_COLOR = color


def next_states(state):
    global One
    states = []
    for string_state in state.getPossibleActions():
        states.append(state.takeAction(string_state))
        if One:
            One = False

    return states


def alphabeta(state, depth, a, b, maximizingPlayer, individual):
    if depth == 0 or state.isTerminal():
        return EvaluateGenetics.evaluate(state, individual, not ENNEMY_COLOR)
    if maximizingPlayer:
        value = float("-inf")
        for state_children in next_states(state):
            value = max(value, alphabeta(state_children, depth - 1, a, b, False, individual))
            a = max(a, value)
            if a >= b:
                break
        return value
    else:
        value = float("inf")
        for state_children in next_states(state):
            value = min(value, alphabeta(state_children, depth - 1, a, b, True, individual))
            b = min(b, value)
            if a >= b:
                break
        return value


def get_best_action(state, individual):
    best_action = None
    best_value = float("-inf")
    for state_action in state.getPossibleActions():
        value = alphabeta(state.takeAction(state_action), args["depth"], float("-inf"), float("inf"), True, individual)
        if value > best_value:
            best_action = state_action
            best_value = value
    return best_action
