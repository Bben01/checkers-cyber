import concurrent.futures

from alpha_beta_pruning import EvaluateGenetics

ENNEMY_COLOR = True


def next_states(state):
    states = []
    for string_state in state.getPossibleActions():
        states.append(state.takeAction(string_state))

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


def execute_alphabeta(args):
    """
    Execute alphabeta and returns the value.
    This method is the interface between the actual alphabeta method and the executor pool
    :param args: the arguments
    :return: the value returned by the alphabeta method
    """
    return alphabeta(args[0], args[1], args[2], args[3], args[4])


def get_best_action(state):
    best_action = None
    best_value = float("-inf")
    possible_actions = state.getPossibleActions()
    state_actions = [(state.takeAction(state_action), 5, float("-inf"), float("inf"), True) for state_action in possible_actions]

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(execute_alphabeta, state_actions))

    for i, result in enumerate(results):
        if result > best_value:
            best_action = possible_actions[i]
            best_value = result

    # with open(r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\alpha_beta_pruning\Debug", "a") as f:
    #     f.write(f'{best_value}, \t\t{best_action}\n')

    return best_action
