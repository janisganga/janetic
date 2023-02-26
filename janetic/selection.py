from typing import Callable, List
import numpy as np
from janetic.chromosome import Chromosome

class Selection:
  """
  The purpose of selection is to emphasize the fitter individuals in the population 
  in hopes that their offspring will in turn have even higher fitness. 
  Selection has to be balanced with variation from crossover and mutation (the "exploitation/exploration balance"):
    - Too−strong selection means that suboptimal highly fit individuals will take over the population, 
  reducing the diversity needed for further change and progress; 
    - Too−weak selection will result in too−slow evolution. 
  """

  def __init__(self, selection_function: Callable[[List[Chromosome]], List[Chromosome]]) -> None:
    """
    Initializes the Selection class with a given specific selection method.

    Args:
        selection_function (Callable[[List[Chromosome]], List[Chromosome]]): the callable given selection method.
    """
    self.selection_function = selection_function

  def select(self, chromosomes: List[Chromosome]) -> List[Chromosome]:
    """
    Performs the chosen selection method on a given list of chromosomes.

    Args:
        chromosomes (List[Chromosome]): the given list of chromosomes.

    Returns:
        List[Chromosome]: the list of selected chromosomes.
    """
    return self.selection_function(chromosomes)

  @staticmethod
  def roulette_wheel(parents_selection_count: int) -> "Selection":
    """
    The idea behind the method is to choose chromosomes with a probability proportional to their fitness value. 
    The higher the fitness value of a chromosome, the more likely it is to be selected for reproduction.

    Args:
        parents_selection_count (int): the number of parents that should be selected for each generation.

    Returns:
        Selection : the Selection instance of the chosen selection method.
    """
    def selection_function(chromosomes: List[Chromosome]) -> List[Chromosome]:
      """
      The wrapper of the chosen selection method.

      Args:
          chromosomes (List[Chromosome]): the given list of chromosomes.

      Returns:
          List[Chromosome]: the list of selected chromosomes.
      """
      fitness_values = np.array([chromosome.fitness for chromosome in chromosomes])
      # Shift all fitness values to positive values to avoid negative values
      shifted_fitness = fitness_values - np.min(fitness_values) + 1
      # Compute the sum of all fitness values
      fitness_sum = np.sum(shifted_fitness)
      # Compute the probability of selection for each chromosome
      probabilities = shifted_fitness / fitness_sum
      # Select k chromosomes using the roulette wheel method
      selected_indices = np.random.choice(len(chromosomes), size=parents_selection_count, replace=False, p=probabilities)
      selected = [chromosomes[i] for i in selected_indices]
      return selected
    return Selection(selection_function)
