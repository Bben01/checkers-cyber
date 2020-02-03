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
    wins_required = games // 2
    win1 = 0  # number of wins of the first  warrior
    win2 = 0  # number of wins of the second warrior
    color = True  # the color of warrior1
    current_color = True  # the current color
    while True:
        state = State.initial_state()
        # plays one game
        while "non terminal":
            state = state.takeAction(Alphabeta.get_best_action(state, warriors[0] if current_color else warriors[1]))
            if state.isTerminal():
                break
            Alphabeta.change_player()
            current_color = not current_color
        # if the match ends, the other lost
        if current_color == color:
            win1 += 1
        else:
            win2 += 1
        # change the color
        color = not color
        Alphabeta.change_player(False)
        # returns the winner if there is one
        if win1 > wins_required:
            warriors[0].won()
            return warriors[0]
        if win2 > wins_required:
            warriors[1].won()
            return warriors[1]


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
