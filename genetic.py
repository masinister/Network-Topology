import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import product, combinations
from individual import Individual
from test import testone
import os
import math

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
        self.interval = 0.1

    def random_population(self):
        return [self.random_individual() for _ in range(self.pop_size)]

    def random_individual(self, num_edges = None):
        if not num_edges:
            # num_edges = int(np.sqrt(len(self.possible_edges)))
            num_edges = 1
        indices = np.random.choice(len(self.possible_edges), num_edges, replace=False)
        edges = [self.possible_edges[i] for i in indices]
        return Individual(self.nodes, self.layers[0], edges)

    def evaluate_all(self):
        total_conns = (self.layer_sizes[0] * (self.layer_sizes[0] - 1))
        for individual in self.POP:
            if individual.isolated_hosts > 0:
                individual.fitness = -individual.isolated_hosts
            else:
                loss, rtt, conns = testone(individual.topo, self.interval)
                if conns == 0:
                    avg_rtt = 1000
                else:
                    avg_rtt = rtt / conns

                avg_loss = loss / total_conns
                efficiency = 1.0 - float(len(individual.edges))/float(len(self.possible_edges))
                individual.ploss = avg_loss
                individual.rtt = avg_rtt

                if avg_loss == 1:
                    individual.fitness == 0
                else:
                    individual.fitness = efficiency * 100. / (avg_rtt * math.sqrt(avg_loss))
        self.POP.sort(key = lambda i: i.fitness, reverse = True)

        if self.POP[0].ploss < 0.7:
            self.interval = max(self.interval - 0.01, 0.02)
        if self.POP[0].ploss > 0.15:
            self.interval = min(self.interval + 0.01, 0.2)

    def recombine(self, i1, i2):
        e1 = i1.graph.edges
        e2 = i2.graph.edges
        new_edges = []
        for e in self.possible_edges:
            b1 = (e in e1)
            b2 = (e in e2)
            if np.random.rand() < 0.2 * (4*b1 + b2):
                new_edges.append(e)
        return Individual(self.nodes, self.layers[0], new_edges)

    def evolve(self):
        new_pop = [self.POP[0], self.POP[1], self.POP[2]]
        for i in range(len(self.POP)-3):
            j = np.random.choice(np.arange(max(1,i-4), min(len(self.POP), i+4)))
            new_pop.append(self.recombine(self.POP[i], self.POP[j]))
            if np.random.rand() < 0.1:
                for _ in range(4):
                    new_pop[-1] = self.mutate(new_pop[-1])
        self.POP = new_pop

    def mutate(self, ind):
        new_edges = ind.edges[:]
        j = np.random.choice(len(self.possible_edges))
        edge = self.possible_edges[j]
        if edge in new_edges:
            new_edges.remove(edge)
        else:
            new_edges.append(edge)
        return Individual(self.nodes, self.layers[0], new_edges)

    def run(self, generations):
        k=3
        topkfitness = [ [] for _ in range(k) ]
        topkrtt = [ [] for _ in range(k) ]
        topkloss = [ [] for _ in range(k) ]
        for g in range(generations):
            print("Generation {}:".format(g))
            self.evaluate_all()
            print("fitness:", [np.round(i.fitness, 2) for i in self.POP])
            print("rtt:", [np.round(i.rtt, 2) for i in self.POP])
            print("loss:", [np.round(i.ploss, 2) for i in self.POP])

            if g % 10 == 0:
                self.POP[0].draw(g)

            for i in range(k):
                topkfitness[i].append(self.POP[i].fitness)
                topkrtt[i].append(self.POP[i].rtt)
                topkloss[i].append(self.POP[i].ploss)

            self.evolve()

        for i in range(k):
            plt.plot(topkfitness[i], label='{}'.format(i))
        plt.savefig('fitness.png')
        plt.clf()

        for i in range(k):
            plt.plot(topkrtt[i], label='{}'.format(i))
        plt.savefig('rtt.png')
        plt.clf()

        for i in range(k):
            plt.plot(topkloss[i], label='{}'.format(i))
        plt.savefig('loss.png')
        plt.clf()

if __name__ == '__main__':
    opt = TopoOptimizer(32, [8,4,4])
    opt.run(201)
