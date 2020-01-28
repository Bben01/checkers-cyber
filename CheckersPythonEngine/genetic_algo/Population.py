class Population:
    def __init__(self):
        self.size = 16
        self.nb_tournaments = self.size / 4
        self.population = []

    def pick(self, start, size):
        return self.population[start:start + size]
