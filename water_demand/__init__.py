#
# Root of the water_supply module.
# Provides access to all shared functionality.
#


def get_version():
    """ Read version number from water_demand/version """
    import os.path
    root = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root, 'version'), 'r') as f:
        return f.read().strip()


__version__ = get_version()
__version_int__ = tuple([int(x) for x in __version__.split('.')])


def version(formatted=False):
    """
    Returns the version number as a tuple (major, minor, revision).
    If ``formatted=True``, returns a string formatted version (for
    example "water_demand 1.0.0").
    """
    if formatted:
        return 'water_demand v{}'.format(__version__)
    else:
        return __version_int__


from .main import WaterDemand
