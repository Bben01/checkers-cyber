import concurrent.futures
from random import shuffle

from deep_learning_algorithms.MctsMethods import State
from genetic_algo import Alphabeta
from genetic_algo.args import args


nb_games = args["nb_games"]


def game(warriors):
    state = State.initial_state()
    color = True
    nb_turns = 0
    while "state is not terminal":
        state = state.takeAction(Alphabeta.get_best_action(state, warriors[0] if color else warriors[1]))
        nb_turns += 1
        if state.isTerminal():
            break
        Alphabeta.change_player()
        color = not color

    print(f"[INFO]\tThe game lasted {nb_turns} turns")
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
    Organize a bracket tournament and return the winner
    :param participants: list of all individuals
    :return: the 4 individuals that won the tournament
    """
    if len(participants) == 4:
        return participants
    tuple_list = [[participants[i], participants[i + 1]] for i in range(0, len(participants) - 1, 2)]
    survivors = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        results = executor.map(generate_tournament_round, tuple_list)

    for result in results:
        survivors.append(result)
    return tournament(survivors)


def alternalted(participants, tournaments_left=24):
    """
    Organize a all man tournament and return the winner
    :param tournaments_left: the number of tournaments to do
    :param participants: list of all individuals
    :return: the 4 individuals that won the tournament
    """
    if tournaments_left == 0:
        from genetic_algo.Population import Population
        return Population.pick_best(participants, 4)
    shuffle(participants)
    tuple_list = [[participants[i], participants[i + 1]] for i in range(0, len(participants) - 1, 2)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        executor.map(generate_tournament_round, tuple_list)

    return alternalted(participants, tournaments_left - 8)
