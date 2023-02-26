from typing import List
import matplotlib.pyplot as plt

from janetic.population import Population
from janetic.fitness import Fitness
from janetic.selection import Selection
from janetic.crossover import Crossover
from janetic.mutation import Mutation

# One simple example problem that can be solved using genetic algorithms is the "knapsack problem".
# The problem statement is as follows:
# Given a set of items, each with a weight and a value, determine the items to include in a collection (the knapsack)
# so that the total weight is less than or equal to a given limit and the total value is maximized.

# To solve this problem using a genetic algorithm, we could represent each item as a binary string,
# where each bit corresponds to whether the item is included in the knapsack or not.
# Assume that we have a knapsack with a weight capacity of 50 units, and there are 10 items available to be placed into the knapsack.
# Each item has a weight and a value.
# With these inputs, the genetic algorithm would try to find the optimal combination of items that maximizes
# the total value while keeping the total weight less than or equal to 50.

knapsack_capacity = 50

items = {
    1: {'weight': 10, 'value': 60},
    2: {'weight': 20, 'value': 100},
    3: {'weight': 30, 'value': 120},
    4: {'weight': 15, 'value': 80},
    5: {'weight': 5, 'value': 40},
    6: {'weight': 12, 'value': 50},
    7: {'weight': 28, 'value': 70},
    8: {'weight': 7, 'value': 30},
    9: {'weight': 18, 'value': 110},
    10: {'weight': 25, 'value': 90}
}

# chromosome size — Dimension of the chromosome vector. In our case, we have 10 items so the chromosome size is equal to 10.
chromosome_length = 10

# genes_type - Possible values for the chromosomes genes encoding. It can be "binary" or "floating_point".
genes_type = "binary"

# population size — The number of individuals in the population.
population_size = 10000

# parents_selection_count — The number of parents that are selected from the population on the base of the selection.
# The parent count must be less than the population size.
parents_selection_count = 100

# generations_number - The number of generations to go through before the algorithm stops running.
generations_number = 100

# crossover_probability — The probability of crossover i.e., if the child inherits the gene of both parents or 1.
# The value of the probability of crossover in a Python genetic algorithm depends on various factors, including the problem being solved,
# the encoding scheme used, and the size of the population. Generally, a value between 0.6 and 0.9 is commonly used for the crossover
# probability in most genetic algorithms.
# A high value of the probability of crossover implies that the search space is explored more rapidly and can lead to a more diverse population.
# On the other hand, a low value of the probability of crossover can result in slower convergence, but it can help to maintain the
# diversity of the population.
# It's recommended to experiment with different values of the probability of crossover and observe their effect on the convergence
# rate and diversity of the population. The optimal value for the probability of crossover can be different for different problems
# and can also depend on the other parameters of the algorithm.
crossover_probability = 0.75

# mutation_probability — The probability of mutation.
# The value of the probability of mutation in a Python genetic algorithm depends on the problem being solved, the encoding scheme used,
# and the size of the population. Generally, a value between 0.001 and 0.1 is commonly used for the mutation probability in most genetic algorithms.
# A high value of the probability of mutation implies that the search space is explored more extensively, which can help to
# overcome local optima and increase diversity in the population. On the other hand, a low value of the probability of mutation
# can result in slower convergence, but it can help to preserve good solutions that have already been found.
# It's recommended to experiment with different values of the probability of mutation and observe their effect on the convergence
# rate and diversity of the population. The optimal value for the probability of mutation can be different for different problems and
# can also depend on the other parameters of the algorithm. In some cases, a variable mutation probability that increases or decreases
# with time can be more effective than a constant value.
mutation_probability = 0.1

# TODO: Smart initialization

def plot_average_fitness(fitness_average: List[float]) -> None:
    plt.plot(fitness_average)
    plt.title('Fitness over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()


# Initialize population
population = Population(genes_type, population_size, chromosome_length)

# Choose fitness method
weights = [item['weight'] for item in items.values()]
values = [item['value'] for item in items.values()]
fitness_function: Fitness = Fitness.knapsack_fitness(knapsack_capacity, weights, values)

# Choose selection, crossover and mutation methods
selection_function: Selection = Selection.roulette_wheel(parents_selection_count)
crossover_function: Crossover = Crossover.single_point_crossover(crossover_probability)
mutation_function: Mutation = Mutation.flip_mutation(mutation_probability, genes_type)

fitness_average = []
solutions = []

# Evolve the population through multiple generations
for generation in range(generations_number):
    print("generation N°", generation)
    population.evolve(fitness_function, selection_function, crossover_function, mutation_function)
    fittest_chromosome = population.get_fittest_chromosomes()
    solutions.append(fittest_chromosome)
    fitness_average.append(population.get_average_fitness())

# Get only the fittests solutions
max_fitness = max(solutions, key=lambda x: x.fitness).fitness
best_chromosomes = [chromosome for chromosome in solutions if chromosome.fitness == max_fitness]
gene_tuples = set(tuple(chromosome.genes) for chromosome in best_chromosomes)
unique_solutions = [chromosome for chromosome in best_chromosomes if tuple(chromosome.genes) in gene_tuples and not gene_tuples.discard(tuple(chromosome.genes))]

for chromosome in unique_solutions:
    gene_indices = [i+1 for i, gene in enumerate(chromosome.genes) if gene == 1]
    filtered_items = {key: items[key] for key in gene_indices}

    total_weight = sum(item['weight'] for item in filtered_items.values())
    total_value = sum(item['value'] for item in filtered_items.values())
    print("----------------------------")
    print("Solution:")
    print("Items", gene_indices)
    print("Total weight:", total_weight)
    print("Total value:", total_value)

plot_average_fitness(fitness_average)
