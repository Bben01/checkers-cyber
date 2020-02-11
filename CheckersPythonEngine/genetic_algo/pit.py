from deep_learning_algorithms.MctsMethods import State
from genetic_algo import Alphabeta
from genetic_algo.args import args


def game(warriors):
    state = State.initial_state()
    color = True
    while "state is not terminal":
        state = state.takeAction(Alphabeta.get_best_action(state, warriors[0] if color else warriors[1]))
        if state.isTerminal():
            break
        Alphabeta.change_player()
        color = not color
        print("OK")

    print("one game")
    return color


def tournament_round(warriors, games):
    """
    One round of the tournament
    :param warriors: list of 2 participants
    :param games: the number of games to play
    :return: individual, winner of each round
    """
    wins_required = games // 2 + 1
    wins = [0, 0]
    i = 0
    while i < games:
        wins[0 if game(warriors) else 1] += 1
        warriors[0], warriors[1] = warriors[1], warriors[0]
        i += 1

        # returns the winner if there is one
        if wins_required in wins:
            warrior = warriors[wins.index(wins_required)]
            warrior.won()
            return warrior


def generate_tournament(participants):
    """
    Organize a 4 man tournament and return the winner
    :param participants: list of individuals (size = 4)
    :return: the individual that won the tournament
    """
    nb_games = args['nb_games']
    if len(participants) == 1:
        return participants[0]
    tuplelist = [[participants[i], participants[i + 1]] for i in range(0, len(participants) - 1, 2)]
    survivors = []
    for t in tuplelist:
        survivors.append(tournament_round(t, nb_games))
    survivor = generate_tournament(survivors)
    return survivor
