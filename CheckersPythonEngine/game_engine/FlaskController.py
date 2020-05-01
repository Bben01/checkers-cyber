from game_engine import Controller
from game_engine.Jeu import Jeu


def analyse_request(json_request):
    board = load_board(json_request["board"], json_request["is_white_turn"])
    state = Jeu(board, json_request["has_to_play_again"])
    args = json_request["args"]
    func = getattr(Controller, json_request["method"])
    return func(state, *args)


def load_board(board_str, is_white_turn):
    from game_engine.Piece import Piece
    from game_engine.Plateau import Plateau
    plateau = Plateau()
    for position, piece in enumerate(board_str):
        x, y = position // 8, position % 8
        if piece != "E":
            plateau.pieces[x][y] = Piece(piece.lower() == "w", piece.isupper())

    plateau.isWhiteTurn = is_white_turn
    plateau.update_pieces()
    return plateau
