import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import math

# Step 1: Initialization of the Population
def initialize_population(population_size, dimension):
    population = []
    for _ in range(population_size):
        individual = [random.random() for _ in range(dimension)]
        population.append(individual)
    return population

import math

# Step 2: Homogenization Policy of Colonies
def homogenization_policy(colonies, target_value, beta):
    homogenized_colonies = []
    for colony in colonies:
        homogenized_colony = [colony[i] + beta * (target_value[i] - colony[i]) for i in range(len(colony))]
        homogenized_colonies.append(homogenized_colony)
    return homogenized_colonies

# Step 3: Revolution and Sudden Change of Colonies
def revolution(colonies, revolt_prob):
    for i in range(len(colonies)):
        if random.random() < revolt_prob:
            colonies[i] = [random.random() for _ in range(len(colonies[0]))]
    return colonies

# Step 4: Replacement of Colony with Imperialist
def replacement(colonies, imperialists, objective_function):
    new_colonies = []
    for colony, imperialist in zip(colonies, imperialists):
        if objective_function(colony) < objective_function(imperialist):

            new_colonies.append(colony)
        else:
            new_colonies.append(imperialist)
    return new_colonies


def calculate_imperial_power(imperialists, colonies, objective_function, xi):
    imperial_power = []
    for imperialist, imperialist_colonies in zip(imperialists, colonies):
        imperialist_cost = objective_function(imperialist)
        if not imperialist_colonies:
            colonies_cost_mean = 0
        else:
            colonies_cost_mean = sum(objective_function(colony) for colony in imperialist_colonies) / len(imperialist_colonies)
        total_cost = imperialist_cost + xi * colonies_cost_mean
        imperial_power.append(total_cost)

    max_total_cost = max(imperial_power)
    normalized_total_costs = [max_total_cost - total_cost for total_cost in imperial_power]
    total_normalized_cost_sum = sum(normalized_total_costs)
    power = [abs(total_cost / total_normalized_cost_sum) for total_cost in normalized_total_costs]
    return power


# Step 6: Competition between Imperialists
def imperialist_competition(imperialists, imperial_power):
    max_power = max(imperial_power)
    normalized_powers = [power / max_power for power in imperial_power]
    return [abs(power - random.random()) for power in normalized_powers]

# Step 7: Collapse of Empire
def collapse_of_empire(imperialists, colonies, difference_vector):
    min_difference_index = difference_vector.index(min(difference_vector))
    if min_difference_index >= 0:
        del imperialists[min_difference_index]
        del colonies[min_difference_index]
    return imperialists, colonies

# Step 8: Termination Condition
def termination_condition(imperialists):
    return len(imperialists) == 1

# Step 9: End
def end():
    print("Algorithm terminated.")


# Main function to run the algorithm
def imperialist_competitive_algorithm(population_size, dimension, max_iterations, revolt_probability, objective_function, target_value, beta, xi):
    population = initialize_population(population_size, dimension)
    imperialists = initialize_population(population_size, dimension)
    
    mean_costs = []
    min_costs = []
    
    for _ in range(max_iterations):
        colonies = homogenization_policy(population, target_value, beta)
        colonies = revolution(colonies, revolt_probability)
        colonies = replacement(colonies, imperialists, objective_function)
        
        imperial_power = calculate_imperial_power(imperialists, colonies, objective_function, xi)
        difference_vector = imperialist_competition(imperialists, imperial_power)
        
        imperialists, colonies = collapse_of_empire(imperialists, colonies, difference_vector)
        
       # Calculate and store mean and minimum costs
        colony_costs = [objective_function(colony) for colony in colonies]

        mean_costs.append(sum(colony_costs) / len(colonies))
        min_costs.append(min(colony_costs))

        
        if termination_condition(imperialists):
            end()
            return mean_costs, min_costs  # Return mean and minimum costs
    
    end()  # If max_iterations reached without termination condition, print termination message
    return mean_costs, min_costs

population_size = 100
dimension = 2  # Since we have two variables x and y
max_iterations = 100
revolt_probability = 0.1
target_value = [0.5, 0.5]  # Example target value for x and y
beta = 0.1
xi = 0.1
 
def objective_function(coordinates):
    if isinstance(coordinates, (int, float)):
        # If coordinates is a single float, return the function value for that coordinate
        return coordinates * math.sin(4 * coordinates)  # Modify this expression accordingly
    else:
        # If coordinates is a tuple of (x, y), unpack and compute the function value
        x, y = coordinates
        return x * math.sin(4 * x) + y * math.sin(2 * y)



# Example usage
mean_costs, min_costs = imperialist_competitive_algorithm(population_size, dimension, max_iterations, revolt_probability, objective_function, target_value, beta, xi)
print("Mean costs:", mean_costs)
print("Minimum costs:", min_costs)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extracting iteration numbers
iterations = range(1, len(mean_costs) + 1)

# Plotting mean costs
ax.plot(iterations, mean_costs, zs=1, zdir='y', label='Mean Costs', color='b')

# Plotting minimum costs
ax.plot(iterations, min_costs, zs=2, zdir='y', label='Minimum Costs', color='r')

ax.set_xlabel('Iteration')
ax.set_ylabel('Cost Type')
ax.set_zlabel('Cost Value')

plt.legend()
plt.title('Evolution of Mean and Minimum Costs over Iterations')
plt.show()
