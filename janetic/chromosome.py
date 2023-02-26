from typing import List

class Chromosome:
  """
  This class represents a basic chromosome that can be used in a genetic algorithm. 
  It has a genes attribute, which is a list of binary or real-valued genes that make up the chromosome, 
  and a fitness attribute, which represents how well the chromosome performs in the problem domain.
  """

  def __init__(self, genes: List[int] | List[float], fitness: float = 0.0) -> None:
    """
    Initializes the Chromosome object with given genes and fitness score.

    Args:
        genes (List[int] | List[float]): A list of genes (binary or real-valued) that make up the chromosome.
        fitness (float, optional): A fitness score representing how well the chromosome performs in the problem domain. Defaults to 0.0.
    """
    self.genes = genes
    self.fitness = fitness

  @classmethod
  def create_chromosome(cls, genes: List[int] | List[float]) -> "Chromosome":
    """
    Creates a new chromosome from a given gene pool.

    Args:
        genes (List[int] | List[float]): A list of genes for the chromosome.

    Returns:
        Chromosome: A new Chromosome object with random genes from the gene pool.
    """
    return cls(genes)

  @classmethod
  def from_genes(cls, genes: List[int] | List[float]) -> "Chromosome":
    """
    Initializes a new Chromosome object based on an already generated genes list.

    Args:
        genes (List[int] | List[float]): A list of genes for the chromosome.

    Returns:
        Chromosome: A new Chromosome object with random genes from the gene pool.
    """
    return cls(genes)
      
  def get_fitness(self) -> float:
    """
    Gets the Chromosome's fitness value.

    Returns:
        float: the chromosome's fitness value.
    """
    return self.fitness

  def set_fitness(self, fitness: float) -> None:
    """
    Sets the Chromosome's fitness value.

    Args:
        fitness (float): the chromosome's fitness value
    """
    self.fitness = fitness

  def __str__(self) -> str:
    """
    Returns a string representation of the Chromosome object, which could be used for printing or debugging purposes.

    Returns:
        str: the string representation of the Chromosome object.
    """
    return f'Genes: {self.genes}, Fitness: {self.fitness}'

  def __repr__(self) -> str:
    """
    Returns a string representation of each genes in Chromosome object, which could be used for printing or debugging purposes.

    Returns:
        str: the string representation of each genes in Chromosome object.
    """
    return str([str(gene) for gene in self.genes])