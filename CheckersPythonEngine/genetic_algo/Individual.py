import random

from genetic_algo.args import args


class Individual:
    def __init__(self, genes=None):
        if genes is None:
            genes = ([], [])
        self.fitness = 0
        self.genes = genes
        self.geneLength = 8
        self.score = 0

    def fillWeights(self):
        w_min = args["weight_min"]
        w_max = args["weight_max"]
        b_min = args["bias_min"]
        b_max = args["bias_max"]
        for _ in range(self.geneLength):
            self.genes[0].append((random.uniform(w_min, w_max), random.uniform(b_min, b_max)))
            self.genes[1].append((-random.uniform(w_min, w_max), random.uniform(b_min, b_max)))

        return self

    def won(self):
        self.score += 1

    def reset(self):
        self.score = 0

    def __str__(self):
        return f"Individual: score={self.score}"

    def reproduce(self, other):
        new_genes = ([], [])
        for i in range(self.geneLength - 1):
            if random.randint(0, 1) == 1:
                new_genes[0].append(other.genes[0][i])
            else:
                new_genes[0].append(self.genes[0][i])
            if random.randint(0, 1) == 1:
                new_genes[1].append(other.genes[1][i])
            else:
                new_genes[1].append(self.genes[1][i])

        return Individual(new_genes)
