from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement
from game_engine.Jeu import Jeu
from game_engine.Piece import Piece


def can_eat(game_instance: Jeu):
    """
    Sends true through the server if the player can eat a piece, false otherwise
    :type game_instance: The game the client is currently playing
    :return:
    """
    return "true" if ValidMoveMethods.has_something_to_eat(game_instance.plateau.pieces, game_instance.plateau.isWhiteTurn, False) else "false"


def selectable(game_instance: Jeu, x, y, check_normals=False):
    """
    Sends true through the server if the piece is eating, false otherwise
    :param game_instance: The game the client is currently playing
    :param check_normals: whether the method has to check normal moves or not
    :param x: the x position of the piece to check
    :param y: the y position of the piece to check
    """
    try:
        x = int(x)
        y = int(y)
        check_normals = bool(check_normals)
        return "true" if ValidMoveMethods.calculate_eat_positions(game_instance.plateau.pieces, x, y, check_normals, True, False) is not None else "false"
    except ValueError:
        return "null"


def is_white_turn(game_instance: Jeu):
    """
    Sends true through the server if white has to play, false otherwise
    :param game_instance: The game the client is currently playing
    """
    return "true" if game_instance.plateau.isWhiteTurn else "false"


def try_move_piece(game_instance: Jeu, x1, y1, x2, y2, has_to_play_again):
    try:
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        has_to_play_again = has_to_play_again.lower() == "true"
    except ValueError:
        return "null"

    infos = game_instance.plateau.try_move(Deplacement(x1, y1, x2, y2), has_to_play_again)
    commands = game_instance.analize_info(infos)
    return "6" + commands


def generate_board_submethod(game_instance: Jeu, x, y, is_white):
    try:
        x = int(x)
        y = int(y)
        is_white = is_white.lower() == "true"
    except ValueError:
        return "null"
    p = Piece(is_white)
    game_instance.plateau.pieces[x][y] = p
    game_instance.plateau.numWhite += 1 if is_white else 0
    game_instance.plateau.numBlack += 0 if is_white else 1
    return "done"


def ia_play(game_instance: Jeu, has_to_play_again):
    # This is where the ia is called to play
    # Just for now:
    x1 = int(input("x1: "))
    y1 = int(input("y1: "))
    x2 = int(input("x2: "))
    y2 = int(input("y2: "))
    infos = game_instance.plateau.try_move(Deplacement(x1, y1, x2, y2), has_to_play_again)
    return game_instance.analize_info(infos)
