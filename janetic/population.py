import random
from typing import List
import statistics
from janetic.mutation import Mutation
from janetic.chromosome import Chromosome
from janetic.crossover import Crossover
from janetic.fitness import Fitness
from janetic.selection import Selection

class Population():
  """
  The Population class represents a collection of chromosomes that evolve over time through the genetic algorithm process.
  It stores a list of Chromosome objects and provides methods for performing various genetic operations such as selection, 
  crossover, and mutation on these chromosomes to create new generations. The Population class also provides methods for 
  tracking the best and worst performing chromosomes over time. Overall, the Population class serves as the main interface
  for running genetic algorithm simulations and evolving solutions to optimization problems.
  """

  def __init__(self, genes_type: str = "binary", population_size: int = 100, chromosome_length: int = 10) -> None:
    """
    Initializes the Population method to create a new Population object from a given gene type, population size and chromosome length.

    Args:
        genes_type (str, optional): the chosen gene type for the chromosomes. Defaults to "binary".
        population_size (int, optional): an integer representing the number of chromosomes in the population. Defaults to 100.
        chromosome_length (int, optional): an interger representing the number of genes in a single chromosome. Defaults to 10.
    """
    self.chromosomes =  self.generate_new_population(genes_type, population_size, chromosome_length) 
    self.genes_type = genes_type
    self.population_size = population_size

  def generate_new_population(self, genes_type: str = "binary", population_size: int = 100, chromosome_length: int = 10) -> List[Chromosome]:
    """
    Generates a new population, given a gene type, population size and chromosome length.

    Args:
        genes_type (str, optional): the chosen gene type for the chromosomes. Defaults to "binary".
        population_size (int, optional): an integer representing the number of chromosomes in the population. Defaults to 100.
        chromosome_length (int, optional): an interger representing the number of genes in a single chromosome. Defaults to 10.

    Raises:
        ValueError: if the genes type isn't correctly specified.

    Returns:
        List[Chromosome]: a list of chromosomes object representing the new generated population.
    """
    population = []
    if genes_type == "binary":
      for _ in range(population_size):
        genes = [random.choice([0, 1]) for _ in range(chromosome_length)]
        population.append(Chromosome.create_chromosome(genes))
    elif genes_type == "floating_point":
      genes = [random.uniform(0, 1) for _ in range(chromosome_length)]
    else:
      raise ValueError('Genes type value should either be "binary", "floating_point" or empty.')
    return population

  def compute_fitness(self, fitness_function: Fitness) -> None:
    """
    Computes the fitness value of each chromosome with the specified fitness computation method.

    Args:
        fitness_function (Fitness)): the callable given fitness computation method.
    """
    for chromosome in self.chromosomes:
      fitness = fitness_function.evaluate(chromosome)
      chromosome.set_fitness(fitness)

  def get_fittest_chromosomes(self, k: int = 1) -> List[Chromosome] | Chromosome:
    """
    Gets the best Chromosome objects in the population based on their fitness values.

    Args:
        k (int, optional): the number of chromosomes that needs to be returned. Defaults to 1.

    Returns:
        List[Chromosome]: the list of the chromosome objects with the highest fitness values in the population.
    """
    sorted_population = sorted(self.chromosomes, key=lambda chromosome: chromosome.fitness, reverse=True)
    return sorted_population[:k] if k > 1 else sorted_population[0]


  def get_least_fit_chromosomes(self, k: int = 1) -> List[Chromosome]:
    """
    Gets the least fit Chromosome objects in the population based on their fitness values.

    Args:
        k (int, optional): the number of chromosomes that needs to be returned. Defaults to 1.

    Returns:
        List[Chromosome]:  the list of the chromosome objects with the lowest fitness values in the population.
    """
    sorted_population = sorted(self.chromosomes, key=lambda chromosome: chromosome.fitness, reverse=False)
    return sorted_population[:k]

  def get_average_fitness(self) -> float:
    """
    Gets the average fitness value of the chromosomes in the population.

    Returns:
        float: the average fitness value of all chromosomes in population.
    """
    fitnesses = [chromosome.fitness for chromosome in self.chromosomes]
    return statistics.fmean(fitnesses)

  def perform_selection(self, selection_method: Selection) -> List[Chromosome]:
    """
    Performs selection operation on the population with the given selection method and return the selected Chromosome objects.

    Args:
        selection_method (Selection]): the callable given selection method.

    Returns:
        List[Chromosome]: the list of selected chromosomes.
    """
    selection_pool = selection_method.select(self.chromosomes)
    return selection_pool

  def perform_crossover(self, mating_pool: List[Chromosome], crossover_function: Crossover) -> List[Chromosome]:
    """
    Performs crossover on the population with the given crossover method and probability.

    Args:
        mating_pool (List[Chromosome]): the selected mating pool of chromosomes.
        crossover_function (Crossover): the callable given crossover method.

    Returns:
        List[Chromosome]: the generated pool of offsprings chromosomes.
    """
    offsprings_pool = []
    for _ in range(len(mating_pool)):
      parents = random.choices(mating_pool, k=2)
      offsprings = crossover_function.cross_over(parents)
      offsprings_pool += offsprings
    return offsprings_pool
  
  def mutate(self, offsprings_pool: List[Chromosome], mutation_function: Mutation) -> List[Chromosome]:
    """
    Performs mutation on the population with the given mutation method and probability.

    Args:
        offsprings_pool (List[Chromosome]): the given pool of offsprings chromosomes.
        mutation_function (Mutation): the callable given mutation method.

    Returns:
        List[Chromosome]: the mutated pool of offsprings chromosomes.
    """
    mutated_pool = []
    for i in range(len(offsprings_pool)):
      mutated_chromosome = mutation_function.perform_mutation(offsprings_pool[i])
      mutated_pool.append(mutated_chromosome)
    return mutated_pool

  def evolve(self, fitness_function: Fitness, selection_function: Selection, crossover_function: Crossover, mutation_function: Mutation) -> List[Chromosome]: 
    """
    Evolves the population for one generation by performing selection, crossover, and mutation operations, 
    and returns the new Population object.

    Args:
        fitness_function (Fitness): the callable given fitness computation method.
        selection_function (Selection): the callable given selection method.
        crossover_function (Crossover): the callable given crossover method.
        mutation_function (Mutation): the callable given mutation method.

    Returns:
        List[Chromosome]: the list of generated chromosomes representing the new population.
    """
    # Evaluate fitness of all chromosomes in population
    self.compute_fitness(fitness_function)
    # Perform mating pool selection
    mating_pool = self.perform_selection(selection_function)
    # Perform crossover and mutation on offsprings
    offsprings_pool = self.perform_crossover(mating_pool, crossover_function)
    mutated_pool = self.mutate(offsprings_pool, mutation_function)
    # Replace the least fit chromosomes by the new offsprings
    new_population = self.remove_chromosomes(self.get_least_fit_chromosomes(len(mutated_pool)))
    new_population += mutated_pool
    self.chromosomes = new_population
    return self.chromosomes

  def remove_chromosomes(self, chromosomes_to_remove: List[Chromosome]) -> List[Chromosome]:
    """
    Removes the chosen chromosomes from the population's chromosomes list. 

    Args:
        chromosomes_to_remove (List[Chromosome]): the chromosomes objects that need to be removed from population.

    Returns:
        List[Chromosome]: the population's chromosomes list without the removed chromosomes.
    """
    return [chromosome for chromosome in self.chromosomes if chromosome not in chromosomes_to_remove]

  def __str__(self) -> str:
    """
    Returns a string representation of the Population object, which could be used for printing or debugging purposes

    Returns:
        str: the string representation of the Population object.
    """
    chromosomes = [str(item) for item in self.chromosomes]
    return f'Chromosomes: {chromosomes}'