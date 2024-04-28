import random

class ImperialistCompetitiveAlgorithm:
    def __init__(self, num_countries, num_dimensions, max_iter, lower_bound, upper_bound):
        self.num_countries = num_countries  # Number of countries
        self.num_dimensions = num_dimensions 
        self.max_iter = max_iter  # Maximum iterations
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.population = None
        self.imperialists = None  # Imperialists
        self.colonies = None   # Colonies
        self.imperialist_costs = None  # Costs of imperialists
        self.colonies_costs = None  # Costs of colonies
        self.best_solution = None  
        self.best_cost = float('inf')

    # Step 1: Initialization of the Population
    def initialize_population(self):
        self.population = [[random.uniform(self.lower_bound, self.upper_bound) for _ in range(self.num_dimensions)] 
                           for _ in range(self.num_countries)]
        self.imperialists = self.population.copy()
        self.colonies = [[0] * self.num_dimensions for _ in range(self.num_countries)]
        self.imperialist_costs = [float('inf')] * self.num_countries
        self.colonies_costs = [float('inf')] * self.num_countries

    # Step 5: Evaluation of the Population
    def evaluate_population(self, objective_function):
        for i in range(self.num_countries):
            cost = objective_function(self.population[i])
            if cost < self.imperialist_costs[i]:
                self.imperialist_costs[i] = cost
                self.imperialists[i] = self.population[i]
        self.best_cost = min(self.imperialist_costs)
        self.best_solution = self.imperialists[self.imperialist_costs.index(self.best_cost)]

    # Step 2: Update Colonies
    def update_colonies(self):
        for i in range(self.num_countries):
            for j in range(self.num_countries):
                if i != j:
                    if self.imperialist_costs[i] > self.imperialist_costs[j]:
                        self.colonies[i] = self.population[j]
                        self.colonies_costs[i] = self.imperialist_costs[j]

    # Step 3: Update Imperialists
    def update_imperialists(self):
        for i in range(self.num_countries):
            if random.random() < 0.5:
                delta = [random.uniform(-1, 1) for _ in range(self.num_dimensions)]
                self.imperialists[i] = [x + delta[idx] for idx, x in enumerate(self.imperialists[i])]

    # Step 4: Replacement of Colony and Imperialist
    def replace_colony_and_imperialist(self):
        for i in range(self.num_countries):
            if random.random() < 0.3:  # Arbitrary probability for replacement
                random_idx = random.randint(0, self.num_countries - 1)
                self.imperialists[i] = self.population[random_idx]

    # Step 6: Colonial Competition
    def colonial_competition(self):
        for i in range(self.num_countries):
            if random.random() < 0.5:  # Arbitrary probability for competition
                random_idx = random.randint(0, self.num_countries - 1)
                if self.imperialist_costs[i] < self.colonies_costs[random_idx]:
                    self.colonies[i] = self.imperialists[i]

    # Step 7: Collapse of the Empire
    def empire_collapse(self):
        for i in range(self.num_countries):
            if random.random() < 0.1:  # Arbitrary probability for collapse
                self.imperialist_costs[i] = float('inf')

    # Step 8: Termination Condition
    def termination_condition(self):
        if self.best_cost < 1e-5:  # Arbitrary termination criterion
            return True
        return False

    # Step 9: Termination
    def optimize(self, objective_function):
        self.initialize_population()
        for _ in range(self.max_iter):
            self.evaluate_population(objective_function)
            self.update_colonies()
            self.update_imperialists()
            self.replace_colony_and_imperialist()  # Step 4
            self.colonial_competition()  # Step 6
            self.empire_collapse()  # Step 7
            if self.termination_condition():  # Step 8
                break
        return self.best_solution, self.best_cost

def sphere_function(x):
    return sum(xi**2 for xi in x)

num_countries = 5
num_dimensions = 5
max_iter = 200
lower_bound = -8
upper_bound = 5

ica = ImperialistCompetitiveAlgorithm(num_countries, num_dimensions, max_iter, lower_bound, upper_bound)
best_solution, best_cost = ica.optimize(sphere_function)
print("Best solution:", best_solution)
print("Best cost:", best_cost)
