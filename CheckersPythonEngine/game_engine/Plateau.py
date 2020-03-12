from game_engine import ValidMoveMethods
from game_engine.Deplacement import Deplacement
from game_engine.InformationCoup import InformationCoup
from game_engine.TourDeJeu import TourDeJeu


class Plateau:
    taillePlateau = 8
    pieces: [[]]

    historique = []

    currentTourDeJeu: TourDeJeu

    isWhiteTurn: bool

    # Keeps track of the number of pieces on-board
    numWhite: int
    numBlack: int

    def __init__(self):
        self.pieces = [[None for _ in range(self.taillePlateau)] for _ in range(self.taillePlateau)]
        self.isWhiteTurn = True
        self.numBlack = 0
        self.numWhite = 0
        self.currentTourDeJeu = None

    @staticmethod
    def out_of_bounds(x: int, y: int):
        return x < 0 or y < 0 or x >= Plateau.taillePlateau or y >= Plateau.taillePlateau

    @staticmethod
    def occupied(board: [], x: int, y: int):
        try:
            return board[x][y] is not None
        except IndexError:
            return True

    def try_move(self, d: Deplacement, has_to_eat_again: bool, last_deplacement=True):
        status = ValidMoveMethods.valid_move(self.pieces, d, has_to_eat_again)
        if self.currentTourDeJeu is None:
            self.currentTourDeJeu = TourDeJeu()

        # Didn't move
        if status.didntMove:
            return InformationCoup.create_didnt_move()

        # Invalid move
        if not status.validMove:
            return InformationCoup.create_invalid_move(status.errorMessage)
        else:
            is_new_queen = not self.pieces[d.origin[0]][d.origin[1]].isKing and \
                           ValidMoveMethods.check_new_queen(d, self.isWhiteTurn) and last_deplacement
            # Killed
            if status.killed:
                p_killed = self.get_killed_piece(d)
                self.numWhite -= 0 if self.isWhiteTurn else 1
                self.numBlack -= 1 if self.isWhiteTurn else 0
                self.move_piece_board(d)

                # If the player does not have to eat again
                if ValidMoveMethods.calculate_eat_positions(self.pieces, d.destination[0], d.destination[1], False,
                                                            True, True) is None:
                    return InformationCoup.create_kill_move(status.killPosition, False, d, p_killed).add_new_queen(
                        is_new_queen, ValidMoveMethods.pos_new_queen(is_new_queen, d))
                else:
                    self.currentTourDeJeu.add_deplacement(d)
                    return InformationCoup.create_kill_move(status.killPosition, True, d, p_killed).add_new_queen(
                        is_new_queen, ValidMoveMethods.pos_new_queen(is_new_queen, d))

            # Normal move
            if status.normalMove:
                self.move_piece_board(d)
                return InformationCoup.create_normal_move(d).add_new_queen(is_new_queen,
                                                                           ValidMoveMethods.pos_new_queen(is_new_queen,
                                                                                                          d))

        return InformationCoup.create_invalid_move("something went wrong...")

    @staticmethod
    def update_piece_board(board: [[]], d: Deplacement):
        board[d.destination[0]][d.destination[1]] = board[d.origin[0]][d.origin[1]]
        board[d.origin[0]][d.origin[1]] = None
        eaten = d.eaten_piece()
        if eaten is not None:
            board[eaten[0]][eaten[1]] = None
        return board

    def move_piece_board(self, d: Deplacement):
        self.pieces = self.update_piece_board(self.pieces, d)
        print("Piece moved")

    def get_killed_piece(self, d: Deplacement):
        eaten = d.eaten_piece()
        return self.pieces[eaten[0]][eaten[1]] if eaten is not None else None

    def end_turn(self, last_deplacement: Deplacement):
        if self.currentTourDeJeu is None:
            return
        self.currentTourDeJeu.add_deplacement(d=last_deplacement)
        self.isWhiteTurn = not self.isWhiteTurn
        self.historique.append(self.currentTourDeJeu)
        self.currentTourDeJeu = None

    def has_pieces_left(self, check_white: bool):
        return self.numWhite != 0 if check_white else self.numBlack != 0
