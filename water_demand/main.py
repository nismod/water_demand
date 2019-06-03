from typing import Union, Sequence
from numbers import Number

import numpy as np


class WaterDemand:
    """
    Simulate water demand based on a linear relationship between
    population size and water demand.  This class is constructed with
    a sequence representing populations at arbitrary nodes (e.g. LADs)
    and a number or sequence of numbers by which to scale those
    populations.
    """

    def __init__(
            self,
            population: Sequence[Number],
            scale_factor: Union[Number, Sequence[Number]],
    ):
        """
        Create a WaterDemand object with given population and scale.

        :param population: A sequence of numbers representing the
          population at each of a number of nodes, e.g. LADs
        :param scale_factor: A single number, or a sequence of numbers
          the same length as the population, representing the linear
          relationship between population and demand at each population
          node.
        """
        self._population = np.asarray(population)

        try:
            len(scale_factor)
            self._scale_factor = np.asarray(scale_factor)
        except TypeError:
            self._scale_factor = np.asarray([scale_factor])

        if len(self._scale_factor) not in [1, len(self._population)]:
            raise ValueError(
                "The scale factor must either be a number, or a list "
                "that is the same length as the population"
            )

    def simulate(self) -> np.ndarray:
        """
        Scale the population by the scale factor, and return the water
        demand.

        :return: the product of population and scale factor
        """
        return self._population * self._scale_factor
