import water_demand


def test_version():
    assert water_demand.version() == (2, 1, 1)
    assert(water_demand.version(formatted=True) == 'water_demand v2.1.1')
