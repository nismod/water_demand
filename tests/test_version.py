import water_demand


def test_version():
    assert water_demand.version() == (0, 0, 1)
    assert(water_demand.version(formatted=True) == 'water_demand v0.0.1')
