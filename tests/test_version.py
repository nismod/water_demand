import water_demand


def test_version():
    assert water_demand.version() == (1, 1, 0)
    assert(water_demand.version(formatted=True) == 'water_demand v1.1.0')
