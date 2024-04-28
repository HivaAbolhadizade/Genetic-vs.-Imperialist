import math
import random


class BGA:
    def __init__(self, target_func, fitness_func, crossover_rate, mutation_rate, population, dimension, generations,
                 domains):
        self.func = target_func
        self.fit = fitness_func
        self.population = population  # population size
        self.population_arr = list()
        self.dim = dimension  # number of parameters
        self.chromosome_len = 0
        self.Pc = crossover_rate
        self.Pm = mutation_rate
        self.generations = generations  # number of generations
        self.best_so_far = 0
        self.L = list()  # length of each parameter
        self.domains = domains  # domain of each parameter: list of dictionaries

    def params_precision_calc(self, delta=0.001):
        for dom in self.domains:
            res = math.ceil(math.log2((dom['high'] - dom['low']) / (delta * 2)))
            self.L.append(res)
        self.chromosome_len = sum(self.L)

    def population_generator(self):
        for i in range(self.population):
            chromosome = list()
            for j in range(self.chromosome_len):
                chromosome.append(random.randint(0, 1))

            self.population_arr.append(chromosome)

    def chromosome_decoding(self):
        decimal_arr = list()
        # divide to Gens
        # binary to decimal
        # normal form
        # real number
        return decimal_arr

    def roulette_wheel_selection(self, fitness_values):
        total_fitness = sum(fitness_values)
        probs = [f / total_fitness for f in fitness_values]
        selected_parents = random.choices(range(self.population), weights=probs, k=self.population)
        return selected_parents

    def one_point_crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.chromosome_len - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        return offspring1, offspring2

    def two_point_crossover(self, parent1, parent2):
        cp1, cp2 = sorted(random.sample(range(1, self.chromosome_len), 2))
        offspring1 = parent1[:cp1] + parent2[cp1:cp2] + parent1[cp2:]
        offspring2 = parent2[:cp1] + parent1[cp1:cp2] + parent2[cp2:]
        return offspring1, offspring2

    def mutation(self):
        for chromosome in self.population_arr:
            if random.random() < self.Pm:
                mutation_position = random.choice(range(1, len(chromosome)))
                chromosome[mutation_position] = 1 - chromosome[mutation_position]
