from genetic_algo import Helper, pit
from genetic_algo.Population import Population
import random

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

    # TODO: faire quelque chose de plus generique, plus DRY
    Helper.swap(selected[0].genes[0], selected[1].genes[0], limit_ally)
    Helper.swap(selected[2].genes[0], selected[3].genes[0], limit_ally)
    Helper.swap(selected[0].genes[1], selected[1].genes[1], limit_enemy)
    Helper.swap(selected[2].genes[1], selected[3].genes[1], limit_enemy)


def mutation():
    for individual in selected:
        if random.randint(1, 101) <= 100 * args["mutation_rate"]:  # 1/rate chance de muter
            for i in range(len(individual.genes)):
                individual.genes[i] = Helper.mutate_list(individual.genes[i])


def main():
    global generation_count
    while generation_count < 400:
        generation_count += 1

        selection()

        crossover()

        mutation()

        print(f"Generation {generation_count}")  # TODO: afficher fittest


if __name__ == '__main__':
    main()
