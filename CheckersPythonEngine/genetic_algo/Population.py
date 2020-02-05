import os
import random
import pickle

from genetic_algo.Individual import Individual


class Population:
    def __init__(self, population=None):
        if population is None:
            population = []
        self.size = 16
        self.nb_tournaments = self.size // 4
        self.population = population

    def pick(self, start, size):
        return self.population[start:start + size]

    def create(self):
        for i in range(self.size):
            individual = Individual()
            self.population.append(individual.fillWeights())

    def fill_reproduce(self, selected):
        """
        Refill the population with reproduction from the selected individuals
        :param selected: the selected individuals
        :return: the population
        """
        new_population = selected
        for i in range(self.size - len(selected)):
            selected_randoms = random.randint(0, len(selected) - 1), random.randint(0, len(selected) - 1)
            new_population.append(selected[selected_randoms[0]].reproduce(selected[selected_randoms[1]]))

        return Population(new_population)

    def best_score(self):
        return max(self.population, key=lambda individual: individual.score)

    def save_fit(self):
        best_individual = self.best_score()
        with open(r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\genetic_algo\serialized", 'wb') as f:
            pickle.dump(best_individual.genes, f)

        with open(r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\genetic_algo\fittest", 'w') as f:
            f.write(str(best_individual.genes))

    def save_population(self):
        best_sort = sorted(self.population, key=lambda individuals: individuals.score)

        for i, individual in enumerate(best_sort):
            with open(fr"../Temp/{i}", "wb") as f:
                pickle.dump(individual, f)

    def __len__(self):
        return len(self.population)

    def load_population(self):
        i = 0
        while True:
            if os.path.isfile(fr"../Temp/{i}"):
                with open(fr"../Temp/{i}", "rb") as f:
                    self.population.append(pickle.load(f))
            else:
                return

    @staticmethod
    def is_saved():
        return os.path.isfile(r"../Temp/0")
