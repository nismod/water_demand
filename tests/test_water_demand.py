import numpy as np

import pytest

from water_demand import WaterDemand


def test_valid_construction():
    """ Test ways in which we expect the class to be used. """

    # Valid ways of specifying population
    p_i = [1, 2, 3, 4]
    p_f = [1.0, 2.0, 3.0, 4.0]
    p_np = np.asarray([1.0, 2.0, 3.0, 4.0])

    # Valid ways of specifying per capita demand
    per_f = 5.0
    per_fs = [5.0] * len(p_f)
    per_np = np.asarray([5.0] * len(p_f))

    # Valid ways of specifying constant demand
    c_f = 2.0
    c_fs = [2.0] * len(p_f)
    c_np = np.asarray([2.0] * len(p_f))

    answer = np.asarray([7.0, 12.0, 17.0, 22.0])

    assert np.array_equal(
        answer, WaterDemand(population=p_i, per_capita_demand=per_f,
                            constant_demand=c_f).simulate()
    )

    assert np.array_equal(
        answer, WaterDemand(population=p_f, per_capita_demand=per_f,
                            constant_demand=c_f).simulate()
    )

    assert np.array_equal(
        answer, WaterDemand(population=p_np, per_capita_demand=per_f,
                            constant_demand=c_f).simulate()
    )

    assert np.array_equal(
        answer, WaterDemand(population=p_np, per_capita_demand=per_fs,
                            constant_demand=c_fs).simulate()
    )

    assert np.array_equal(
        answer, WaterDemand(population=p_np, per_capita_demand=per_np,
                            constant_demand=c_np).simulate()
    )

    assert np.array_equal(
        answer, WaterDemand(population=p_i, per_capita_demand=per_fs,
                            constant_demand=c_np).simulate()
    )


def test_invalid_construction():
    """ Test explicitly invalidated methods of construction """

    pop = [1.23, 2.34, 3.45]

    # Any demand with length not one or three is invalid
    per_2 = [1, 2]
    per_3 = [1, 2, 3]
    per_4 = [1, 2, 3, 4]

    c_2 = [1, 2]
    c_3 = [1, 2, 3]
    c_4 = [1, 2, 3, 4]

    with pytest.raises(ValueError, match=r"The per capita demand must"):
        WaterDemand(
            population=pop,
            per_capita_demand=per_2,
            constant_demand=c_3
        )

    with pytest.raises(ValueError, match=r"The per capita demand must"):
        WaterDemand(
            population=pop,
            per_capita_demand=per_4,
            constant_demand=c_3
        )

    with pytest.raises(ValueError, match=r"The constant demand must"):
        WaterDemand(
            population=pop,
            per_capita_demand=per_3,
            constant_demand=c_2
        )

    with pytest.raises(ValueError, match=r"The constant demand must"):
        WaterDemand(
            population=pop,
            per_capita_demand=per_3,
            constant_demand=c_4
        )


def test_simulate():
    """ Test the most general case with specific values """

    pop = [1.23, 2.34, 3.45, 4.56]
    per_cap = [5.67, 6.78, 7.89, 9.01]
    const = [10.11, 12.13, 13.14, 14.15]

    simulated = WaterDemand(
        population=pop,
        per_capita_demand=per_cap,
        constant_demand=const,
    ).simulate()

    answer = np.asarray([
        1.23 * 5.67 + 10.11,
        2.34 * 6.78 + 12.13,
        3.45 * 7.89 + 13.14,
        4.56 * 9.01 + 14.15,
    ])

    assert (np.array_equal(simulated, answer))
