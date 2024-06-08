import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def calculate_linear_scaling_coefficients(C_m, fit_ave, fit_max):
    if fit_max == fit_ave:
        return 1, 0  
    a = ((C_m - 1) * fit_ave) / (fit_max - fit_ave)
    b = (1 - a) * fit_ave
    return a, b

def scale_fitness(raw_fitness, a, b):
    return a * raw_fitness + b

def linear_scaling(chromosomes, fitness_function, C_m):
    raw_fitness_values = np.array([fitness_function(chromosome) for chromosome in chromosomes])
    fit_ave = np.mean(raw_fitness_values)
    fit_max = np.max(raw_fitness_values)

    a, b = calculate_linear_scaling_coefficients(C_m, fit_ave, fit_max)
    scaled_fitness_values = scale_fitness(raw_fitness_values, a, b)

    return scaled_fitness_values, fit_max, fit_ave


def create_fitness_function(formula):
    x = sp.symbols('x0:%d' % 3)  
    expr = sp.sympify(formula)
    f = sp.lambdify(x, expr, 'numpy')
    return lambda chromosome: f(*chromosome)


user_formula = 'x0 + 2*x1 + 3*x2'  


chromosomes = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [2, 3, 4],
    [5, 6, 7]
]


fitness_function = create_fitness_function(user_formula)

C_m = 1.5  


scaled_fitness_values, fit_max, fit_ave = linear_scaling(chromosomes, fitness_function, C_m)

print("Scaled Fitness Values:", scaled_fitness_values)
print("Max Fitness Value:", fit_max)
print("Average Fitness Value:", fit_ave)


plt.plot(scaled_fitness_values, label='Scaled Fitness')
plt.axhline(y=fit_max, color='r', linestyle='--', label='Max Fitness')
plt.axhline(y=fit_ave, color='g', linestyle='--', label='Average Fitness')
plt.xlabel('Chromosome Index')
plt.ylabel('Fitness Value')
plt.title('Scaled Fitness Values')
plt.legend()
plt.show()
