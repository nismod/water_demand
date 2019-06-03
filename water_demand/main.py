from typing import Union, Sequence
from numbers import Number

import numpy as np


class WaterDemand:

    def __init__(
            self,
            population: Sequence[Number],
            scale_factor: Union[Number, Sequence[Number]],
    ):
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
