import random
from typing import Callable
from janetic import Chromosome

class Mutation:
    """
    The Mutation class defines different mutation operations that can be applied to the candidate
    solutions during the optimization process. 
    The Mutation class is used to introduce diversity into the population and prevent premature
    convergence to suboptimal solutions. By randomly mutating some of the candidate solutions,
    the algorithm can explore new areas of the solution space and potentially discover better solutions.
    """

    def __init__(self, mutation_function: Callable[[Chromosome], Chromosome]) -> None:
        """
        Initializes the Mutation class with a given specific mutation method.

        Args:
            mutation_function (Callable[[Chromosome], Chromosome]): the callable given mutation method.
        """
        self.mutation_function = mutation_function

    def perform_mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        Mutates the genes of the chromosome with a given mutation method.

        Args:
            chromosome (Chromosome): a given chromosome.

        Returns:
            Chromosome: the mutated (or not mutated) chromosome.
        """
        return self.mutation_function(chromosome)

    @staticmethod
    def flip_mutation(mutation_probability: float, genes_type: str) -> "Mutation":
        """
        In the Flip Mutation method, a random bit or gene in the chromosome is selected and flipped (i.e., its value is changed 
        from 0 to 1 or from 1 to 0). This is one of the simplest and most commonly used mutation methods.
        Although a few other schemes have been occasionally used, the most common mutation operator for binary encodings
        considers each gene separately and allows each bit to flip with a small probability.

        Args:
            mutation_probability (float): the probability of a gene being mutated.
            genes_type (str): the name of the genes types.

        Returns:
            Mutation: the Mutation instance of the chosen mutation method.
        """
        def mutation_function(chromosome: Chromosome) -> Chromosome:
            """
            The wrapper of the chosen mutation method.

            Args:
                chromosome (Chromosome): a given chromosome.

            Raises:
                ValueError: if the genes type isn't correctly specified.

            Returns:
                Chromosome: the mutated (or not mutated) chromosome.
            """
            for i in range(len(chromosome.genes)):
                if random.random() < mutation_probability:
                    if genes_type == "binary":
                        mutated_gene = int(random.uniform(0, 1))
                    elif genes_type == "floating_point":
                        mutated_gene = random.choice([0, 1])
                    else:
                        raise ValueError('Genes type value should either be "binary", "floating_point" or empty.')
                    chromosome.genes[i] = mutated_gene
            return chromosome

        return Mutation(mutation_function)
