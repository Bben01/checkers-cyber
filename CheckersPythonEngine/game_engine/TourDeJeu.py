from game_engine import Deplacement


class TourDeJeu:
    deplacements = []
    codeError: int
    success: bool

    def __init__(self):
        self.codeError = -1
        self.success = False

    def add_deplacement(self, d: Deplacement):
        self.deplacements.append(d)
        self.success = True
        return True

    def set_code_error(self, code: int):
        self.codeError = code
