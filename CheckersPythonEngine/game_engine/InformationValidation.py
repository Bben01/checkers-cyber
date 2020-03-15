class InformationValidation:
    validMove: bool
    killed: bool
    didntMove: bool
    normalMove: bool
    killPosition: tuple
    errorMessage: str

    def __init__(self, valid_move: bool, killed: bool, didnt_moved: bool, normal_move: bool, kill_position: tuple, error_message: str):  # NOQA
        self.validMove = valid_move
        self.killed = killed
        self.didntMove = didnt_moved
        self.normalMove = normal_move
        self.killPosition = kill_position
        self.errorMessage = error_message

    @staticmethod
    def create_normal_move():
        return InformationValidation(True, False, False, True, (), "")

    @staticmethod
    def create_kill_move(kill_position: tuple):
        return InformationValidation(True, True, False, False, kill_position, "")

    @staticmethod
    def create_not_move():
        return InformationValidation(False, False, True, False, (), "the piece didn't move.")

    @staticmethod
    def create_wrong_move(error_message: str):
        return InformationValidation(False, False, False, False, (), error_message)
