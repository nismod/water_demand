from typing import Union, Sequence
from numbers import Number

import numpy as np


class WaterDemand:
    """
    Simulate water demand based on a linear relationship between
    population size and water demand, plus a constant demand.

    This class is constructed with a sequence representing populations
    at arbitrary nodes (e.g. water resource zones), a number or sequence
    of numbers representing per capita water demand, and a number or
    sequence of numbers representing a constant water demand.

    Water demand is calculated as const + per_capita * population.
    """

    def __init__(
            self,
            population: Sequence[Number],
            per_capita_demand: Union[Number, Sequence[Number]],
            constant_demand: Union[Number, Sequence[Number]]
    ):
        """
        Create a WaterDemand object with given population and scale.

        :param population: A sequence of numbers representing the
          population at each of a number of nodes, e.g. water resource
          zones.
        :param per_capita_demand: A single number, or a sequence of
          numbers the same length as the population, representing the
          per capita demand for water.
        :param constant_demand: A single number, or a sequence of
          numbers the same length as the population, representing the
          constant demand for water.
        """
        self._population = np.asarray(population)

        try:
            len(per_capita_demand)
            self._per_capita_demand = np.asarray(per_capita_demand)
        except TypeError:
            self._per_capita_demand = np.asarray([per_capita_demand])

        try:
            len(constant_demand)
            self._const_demand = np.asarray(constant_demand)
        except TypeError:
            self._const_demand = np.asarray([constant_demand])

        if len(self._per_capita_demand) not in [1, len(self._population)]:
            raise ValueError(
                "The per capita demand must either be a number, or a"
                "list that is the same length as the population"
            )

        if len(self._const_demand) not in [1, len(self._population)]:
            raise ValueError(
                "The constant demand must either be a number, or a"
                "list that is the same length as the population"
            )

    def simulate(self) -> np.ndarray:
        """
        Scale the population by the per capita demand, add the constant
        demand, and return this as the water demand.

        :return: the product of population and scale factor
        """
        return self._const_demand + self._population * self._per_capita_demand
