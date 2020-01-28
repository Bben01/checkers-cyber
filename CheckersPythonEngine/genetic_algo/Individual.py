import random
from genetic_algo.main import args


class Individual:
    def __init__(self):
        self.fitness = 0
        self.genes = ([], [])
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
