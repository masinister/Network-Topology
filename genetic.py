import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
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

    def random_individual(self, num_edges = None):
        if not num_edges:
            num_edges = int(np.sqrt(len(self.possible_edges)))
        indices = np.random.choice(len(self.possible_edges), num_edges, replace=False)
        edges = [self.possible_edges[i] for i in indices]
        return Individual(self.nodes, self.layers[0], edges)

    def evaluate_all(self):
        conns = (self.layer_sizes[0] * (self.layer_sizes[0] - 1))
        for individual in self.POP:
            if individual.isolated_hosts:
                individual.fitness = 0
            else:
                loss, rtt = testone(individual.topo)
                avg_rtt = rtt / conns
                avg_loss = loss / conns
                throughput = 1.0 - loss / conns
                efficiency = 1.0 - float(len(individual.edges))/float(len(self.possible_edges))

                if avg_rtt == 0 or avg_loss == 1:
                    individual.fitness == 0
                else:
                    individual.fitness = 100. / (avg_rtt**2 * avg_loss)
        self.POP.sort(key = lambda i: i.fitness, reverse = True)

    def recombine(self, i1, i2):
        e1 = i1.graph.edges
        e2 = i2.graph.edges
        new_edges = []
        for e in self.possible_edges:
            b1 = (e in e1)
            b2 = (e in e2)
            if np.random.rand() < 0.5 * (b1 + b2):
                new_edges.append(e)
        return Individual(self.nodes, self.layers[0], new_edges)

    def evolve(self):
        new_pop = [self.POP[0], self.POP[1], self.POP[2]] + [self.random_individual()]*3
        for i in range(len(self.POP)-6):
            j = np.random.choice(np.arange(max(1,i-4), min(len(self.POP), i+4)))
            new_pop.append(self.recombine(self.POP[i], self.POP[j]))
            if self.POP[i].fitness == 0 or np.random.rand() < 0.2:
                for _ in range(2):
                    self.mutate(i)
        self.POP = new_pop

    def mutate(self, i):
        e1 = self.POP[i].edges
        new_edges = e1
        j = np.random.choice(len(self.possible_edges))
        edge = self.possible_edges[j]
        if edge in new_edges:
            new_edges.remove(edge)
        else:
            new_edges.append(edge)
        self.POP[i] = Individual(self.nodes, self.layers[0], new_edges)

    def run(self, generations):
        top10fitness = [[]]*10
        for g in range(generations):
            print("Generation {}:".format(g))
            self.evaluate_all()
            print([np.round(i.fitness, 2) for i in self.POP])

            if g % 10 == 0:
                self.POP[0].draw(g)

            for i in range(10):
                top10fitness[i].append(self.POP[i].fitness)

            self.evolve()



        for i in range(10):
            plt.plot(top10fitness[i])
        plt.savefig('fitness.png')

if __name__ == '__main__':
    opt = TopoOptimizer(32, [8,8,8])
    opt.run(101)
