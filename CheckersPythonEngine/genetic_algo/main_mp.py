args = {
    "mutation": 0.1,
    "mutation_rate": 0.5,
    "mutation_deviation": 0.1,
    "weight_min": 0,
    "weight_max": 10,
    "bias_min": -10,
    "bias_max": 10,
    "depth": 2,
    "reproduce_winner": 3,
    "nb_games": 3
}

from genetic_algo import Helper, pit_mp
from genetic_algo.Population import Population
import random


population = Population()
selected = []
generation_count = 0


def selection():
    global selected
    random.shuffle(population.population)
    selected.extend(pit_mp.tournament(population.population))


def crossover():
    limit_ally = random.randint(0, selected[0].geneLength - 1)
    limit_enemy = random.randint(0, selected[0].geneLength - 1)

    previous = None
    for individual in selected:
        if previous is None:
            previous = individual
            continue
        Helper.swap(previous.genes[0], individual.genes[0], limit_ally)
        Helper.swap(previous.genes[1], individual.genes[1], limit_enemy)
        previous = None


def mutation():
    for individual in population.population:
        if random.randint(1, 101) <= 100 * args["mutation_rate"]:  # 1/rate chance de muter
            individual.genes = Helper.mutate_list(individual.genes[0]), Helper.mutate_list(individual.genes[1])


def main():
    global generation_count, population, selected
    if Population.is_saved():
        population.load_population()
    else:
        population.create()
    while True:
        generation_count += 1

        selection()

        crossover()

        population = population.fill_reproduce(selected)

        selected = []

        mutation()

        print(f"Generation {generation_count}: {population.best_score()}")

        population.save_fit()

        population.save_population()


if __name__ == '__main__':
    main()
