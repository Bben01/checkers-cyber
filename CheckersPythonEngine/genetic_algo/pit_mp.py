import concurrent.futures

from deep_learning_algorithms.MctsMethods import State
from genetic_algo import Alphabeta
from genetic_algo.main_mp import args


nb_games = args["nb_games"]


def game(warriors):
    state = State.initial_state()
    color = True
    while "state is not terminal":
        state = state.takeAction(Alphabeta.get_best_action(state, warriors[0] if color else warriors[1]))
        if state.isTerminal():
            break
        Alphabeta.change_player()
        color = not color

    return color


def generate_tournament_round(warriors):
    """
    One round of the tournament
    :param warriors: list of 2 participants
    :return: individual, winner of each round
    """
    wins_required = nb_games // 2 + 1
    wins = [0, 0]
    i = 0
    while i < nb_games:
        wins[0 if game(warriors) else 1] += 1
        warriors[0], warriors[1] = warriors[1], warriors[0]
        i += 1

        # returns the winner if there is one
        if wins_required in wins:
            warrior = warriors[wins.index(wins_required)]
            warrior.won()
            return warrior


def tournament(participants):
    """
    Organize a all man tournament and return the winner
    :param participants: list of all individuals
    :return: the 4 individuals that won the tournament
    """
    if len(participants) == 4:
        return participants
    tuple_list = [[participants[i], participants[i + 1]] for i in range(0, len(participants) - 1, 2)]
    survivors = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(generate_tournament_round, tuple_list)

    for result in results:
        survivors.append(result)
    return tournament(survivors)
