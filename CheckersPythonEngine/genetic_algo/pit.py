from deep_learning_algorithms.MctsMethods import State
from genetic_algo import Alphabeta
from genetic_algo.main import args


def tournament_round(warriors, games):
    """
    One round of the tournament
    :param warriors: tuple of participants
    :param games: the number of games to play
    :return: individual, winner of each round
    """
    win1 = 0  # number of wins of the first  warrior
    win2 = 0  # number of wins of the second warrior
    color = True  # the color of warrior1
    current_color = True  # the current color
    for i in range(games):
        state = State.initial_state()
        while not state.isTerminal():
            state = state.takeAction(Alphabeta.get_best_action(state, warriors[0] if current_color else warriors[1]))
            Alphabeta.change_player()
            current_color = not current_color
        if state.has_won(current_color):



def generate_tournament(participants):
    """
    Organize a 4 man tournament and return the winner
    :param participants: list of individuals (size = 4)
    :return: the individual that won the tournament
    """
    nb_games = args['nb_games']
    if len(participants) == 1:
        return participants[0]
    tuplelist = [(participants[i], participants[i + 1]) for i in range(0, len(participants) - 1, 2)]
    survivors = []
    for t in tuplelist:
        survivors.append(tournament_round(t, nb_games))
    survivor = generate_tournament(survivors)
    return survivor
