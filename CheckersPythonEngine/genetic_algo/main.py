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
    "nb_games": 5
}

from genetic_algo import Helper, pit
from genetic_algo.Population import Population
import random


population = Population()
selected = []
generation_count = 0


def selection():
    global selected
    random.shuffle(population.population)
    for tournament in Helper.split_list(population.population, population.nb_tournaments):
        selected.append(pit.generate_tournament(tournament))


def crossover():
    limit_ally = random.randint(0, selected[0].geneLength)
    limit_enemy = random.randint(0, selected[0].geneLength)

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
    global generation_count, population
    population.create()
    while generation_count < 400:
        generation_count += 1

        selection()

        crossover()

        population = population.fill_reproduce(selected)

        mutation()

        print(f"Generation {generation_count}: {Helper.print_population(selected)}")


if __name__ == '__main__':
    main()
