from random import randint
from typing import Callable, List
from janetic.chromosome import Chromosome

class Crossover:
    """
    The process of crossover is used to create new candidate solutions by combining the genetic material
    from two parent solutions. The crossover process involves selecting a crossover point or points in the 
    parent solutions and swapping the genetic material on either side of that point to create two new child solutions.
    The idea is to randomly decide whether or not to perform crossover between the parent chromosomes based on 
    the crossover probability, and then use the resulting offspring chromosomes in the next generation of the genetic algorithm.
    This class takes two parent solutions as input and uses a specific crossover strategy to generate one or more new child solutions.
    """

    def __init__(self, crossover_function: Callable[[List[Chromosome]], List[Chromosome]]) -> None:
        """
        Initializes the Crossover class with a given specific crossover method.

        Args:
            crossover_function (Callable[[List[Chromosome]], List[Chromosome]]): the callable given crossover method.
        """
        self.crossover_function = crossover_function

    def cross_over(self, parents: List[Chromosome]) -> List[Chromosome]:
        """
        Performs the chosen crossover method on a given list of selected parents chromosomes.

        Args:
            parents (List[Chromosome]): the selected couple of parents chromosomes.

        Returns:
            List[Chromosome]: the generated couple of offsprings chromosomes.
        """
        return self.crossover_function(parents)

    @staticmethod
    def single_point_crossover(crossover_probability: float) -> "Crossover":
        """
        A single point is randomly selected in the chromosome strings of both parents, 
        and the chromosomes are divided at that point. The genetic material from one parent 
        is combined with the genetic material from the other parent after that point, 
        to produce two offspring. Here, the crossover probability is typically used to determine
        whether or not a given pair of parent chromosomes should undergo crossover during reproduction.

        Here's an example of how you might use a crossover probability of 0.8 with single-point crossover in a genetic algorithm:
        - If crossover_prob is less than or equal to 0.8 (the crossover probability), then perform single-point crossover on 
        parent1 and parent2 to create two new offspring chromosomes (e.g., child1 and child2).
        - If crossover_prob is greater than 0.8, then simply use parent1 and parent2 as the two new offspring chromosomes without any crossover.
    

        Args:
            crossover_probability (float): the chosen crossover probability. 

        Returns:
            Crossover: the Crossover instance of the chosen crossover method.
        """
        def crossover_function(parents: List[Chromosome]) -> List[Chromosome]:
            """
            The wrapper of the chosen crossover method.

            Args:
                parents (List[Chromosome]): the list of two parent chromosomes selected from the current population.

            Raises:
                ValueError: if the length of the selected parents chromosomes list is not 2.
                ValueError: if the selected parents chromosomes have differents lengths.
                ValueError: if the crossover probability value isn't between 0 and 1.

            Returns:
                List[Chromosome]: the list containing the generated couple of offsprings chromosomes.
            """
            if len(parents) != 2:
                raise ValueError("Single-point crossover requires exactly 2 parents.")

            if len(parents[0].genes) != len(parents[1].genes):
                raise ValueError("Parents must have the same length.")

            if crossover_probability < 0 or crossover_probability > 1:
                raise ValueError("Crossover probability must be between 0 and 1.")

            # Determine whether to perform crossover
            if randint(0, 1) > crossover_probability:
                return parents
            else:
                # Perform single point crossover
                crossover_point = randint(1, len(parents[0].genes) - 1)
                offspring1 = parents[0].genes[:crossover_point] + \
                    parents[1].genes[crossover_point:]
                offspring2 = parents[1].genes[:crossover_point] + \
                    parents[0].genes[crossover_point:]
                return [Chromosome.from_genes(offspring1), Chromosome.from_genes(offspring2)]
        return Crossover(crossover_function)
