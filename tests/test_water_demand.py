import numpy as np

import pytest

from water_demand import WaterDemand


def test_valid_construction():

    # Valid ways of specifying population
    p_i = [1, 2, 3, 4]
    p_f = [1.0, 2.0, 3.0, 4.0]
    p_np = np.asarray([1.0, 2.0, 3.0, 4.0])

    # Valid ways of specifying scale
    s_f = 5.0
    s_fs = [5.0] * len(p_f)
    s_np = np.asarray([5.0] * len(p_f))

    answer = np.asarray([5.0, 10.0, 15.0, 20.0])

    assert np.array_equal(
        answer, WaterDemand(population=p_i, scale_factor=s_f).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_i, scale_factor=s_fs).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_i, scale_factor=s_np).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_f, scale_factor=s_f).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_f, scale_factor=s_fs).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_f, scale_factor=s_np).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_np, scale_factor=s_f).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_np, scale_factor=s_fs).simulate()
    )
    assert np.array_equal(
        answer, WaterDemand(population=p_np, scale_factor=s_np).simulate()
    )


def test_invalid_construction():

    pop = [1.23, 2.34, 3.45]

    # Any scale with length not one or three is invalid
    s_2 = [1, 2]
    s_4 = [1, 2, 3, 4]

    with pytest.raises(ValueError, match=r"The scale factor must either be a"):
        WaterDemand(pop, s_2)

    with pytest.raises(ValueError, match=r"The scale factor must either be a"):
        WaterDemand(pop, s_4)


def test_simulate():

    pop = [1.23, 2.34, 3.45, 4.56]
    scale = [5.67, 6.78, 7.89, 9.01]

    simulated = WaterDemand(population=pop, scale_factor=scale).simulate()
    answer = np.asarray([1.23 * 5.67, 2.34 * 6.78, 3.45 * 7.89, 4.56 * 9.01])

    assert(np.array_equal(simulated, answer))
