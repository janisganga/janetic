from itertools import compress
from typing import Callable, List, Union
from janetic.chromosome import Chromosome

class Fitness:
    """
    The Fitness class is responsible for defining and evaluating how well a solution solves the optimization problem.
    The function assigns a fitness score to each chromosomes, or candidate solution, which is used by
    the genetic algorithm to select the fittest individuals for reproduction and mutation.
    """

    def __init__(self, fitness_function: Callable[[List[int] | List[float]], float]) -> None:
        """
        Initializes the Fitness class with a given specific fitness computation method.

        Args:
            fitness_function (Callable[[List[int] | List[float]], float]): the callable given fitness computation method.
        """
        self.fitness_function = fitness_function

    def evaluate(self, chromosome: "Chromosome") -> Union[float, int]:
        """
        Performs the chosen fitness computation method on a given chromosome.

        Args:
            chromosome (Chromosome): the given chromosome.

        Returns:
            Union[float, int]: the chromosome's fitness value.
        """
        return self.fitness_function(chromosome.genes)

    @staticmethod
    def knapsack_fitness(capacity: int, weights: List[int], values: List[int]) -> "Fitness":
        """
        This method calculates the fitness score for a candidate solution to a knapsack problem.
        The knapsack problem involves selecting a subset of items to maximize the total value,
        subject to a constraint on the maximum weight.
        This method calculate the total value and weight of the selected items based on the candidate
        solution and compare it to the maximum weight constraint. If the total weight exceeds the constraint,
        the fitness score would be set to zero. 
        Otherwise, the fitness score would be set to the total value of the selected items.

        Args:
            capacity (int): the value indicating the maximum weight capacity of the knapsack.
            weights (List[int]): a list of integers representing the weights of the items.
            values (List[int]): a list of integers representing the values of the items.

        Returns:
            Fitness: the Fitness instance of the chosen fitness computation method.
        """
        def fitness_function(genes: List[int] | List [float]) -> float:
            """
            The wrapper of the chosen fitness computation method.

            Args:
                genes (List[int] | List [float]): a list of given chromosome's genes.

            Returns:
                float: the value of the chromosome's fitness
            """
            total_weight = sum(compress(weights, genes))
            if total_weight > capacity:
                return 0.0
            return sum(compress(values, genes))

        return Fitness(fitness_function)
