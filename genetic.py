import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from individual import Individual
from test import testone

class TopoOptimizer():
    # input:
    #     pop_size: how many individuals in the population
    #     layer_sizes: [num_hosts, num_l1_switches, num_l2_switches ...]
    #     fitness func: returns fitness (float) of an individual
    def __init__(self, pop_size, layer_sizes):
        self.pop_size = pop_size
        self.layer_sizes = layer_sizes
        # Layered Topology
        self.layers = []
        self.possible_edges = []
        for i, size in enumerate(layer_sizes):
            self.layers.append(list(product([i], range(size))))
            if i > 0:
                self.possible_edges.extend(list(combinations(self.layers[i], 2)))
                self.possible_edges.extend(list(product(self.layers[i-1], self.layers[i])))
        self.nodes = sum(self.layers, [])
        self.POP = self.random_population()

    def random_population(self):
        return [self.random_individual() for _ in range(self.pop_size)]

    def random_individual(self):
        num_edges = np.random.choice(int(np.sqrt(len(self.possible_edges))))
        indices = np.random.choice(len(self.possible_edges), num_edges, replace=False)
        edges = [self.possible_edges[i] for i in indices]
        return Individual(self.nodes, self.layers[0], edges)

    def evaluate_all(self):
        for individual in self.POP:
            if individual.isolated_hosts:
                individual.fitness = 0
            else:
                sent, lost = testone(individual.topo)
                throughput = 1.0 - float(lost)/float(sent)
                efficiency = 1.0 - float(len(individual.edges))/float(len(self.possible_edges))
                individual.fitness = throughput + 0.1 * efficiency
        self.POP.sort(key = lambda i: i.fitness, reverse = True)

    def recombine(self, i1, i2):
        e1 = i1.graph.edges
        e2 = i2.graph.edges
        new_edges = []
        for e in self.possible_edges:
                if np.random.rand() < 0.3 * (1 + (e in e1) + (e in e2)):
                    new_edges.append(e)
        return Individual(self.nodes, self.layers[0], new_edges)

    def evolve(self):
        new_pop = [self.POP[0], self.random_individual()]
        for i in range(1, len(self.POP)-1):
            j = np.random.choice(i)
            new_pop.append(self.recombine(self.POP[i], self.POP[j]))
        self.POP = new_pop

    def mutate(self):
        i = np.random.choice(len(self.POP))
        self.POP[i] = self.recombine(self.POP[i], self.random_individual())

    def run(self, generations):
        for g in range(generations):
            print("Generation {}:".format(g))
            self.evaluate_all()
            print([np.round(i.fitness,2) for i in self.POP])
            self.POP[0].draw(g)
            self.evolve()
            self.mutate()

if __name__ == '__main__':
    opt = TopoOptimizer(25, [8,8,8])
    opt.run(10)
