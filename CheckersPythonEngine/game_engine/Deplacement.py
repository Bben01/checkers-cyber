class Deplacement:
    origin: tuple
    destination: tuple

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.origin = (x1, y1)
        self.destination = (x2, y2)

    def eaten_piece(self):
        """

        :return: Returns the position of the eaten piece, if there is no, the return is None.
        """
        sum_x = self.origin[0] + self.destination[0]
        sum_y = self.origin[1] + self.destination[1]
        ok_x = sum_x % 2 == 0
        ok_y = sum_y % 2 == 0
        return (sum_x / 2, sum_y / 2) if ok_x and ok_y else None

    def null_move(self):
        return self.origin == self.destination
