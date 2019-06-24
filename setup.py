#
# water_demand setuptools script
#

import os
import setuptools


def get_description():
    """ Read long description from README.md """
    root = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root, 'README.md')) as f:
        return f.read().strip()


def get_version():
    """ Read version number from water_demand/version """
    root = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root, 'water_demand', 'version'), 'r') as f:
        return f.read().strip()


setuptools.setup(
    # Module name (lowercase)
    name='water_demand',
    version=get_version(),

    # Description
    description='Water demand model for Nismod2',
    long_description=get_description(),
    long_description_content_type="text/markdown",

    # License name
    license='MIT license',

    # Maintainer information
    # author='',
    # author_email='',
    maintainer='Fergus Cooper',
    maintainer_email='fergus.cooper@cs.ox.ac.uk',
    url='https://github.com/nismod/water_demand',

    # Packages to include
    packages=setuptools.find_packages(include='water_demand'),

    # Metadata to help PIP
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # Include non-python files (via MANIFEST.in)
    include_package_data=True,

    # List of dependencies
    install_requires=[
        'numpy>=1.8',
    ],
    extras_require={
        'docs': [
            'sphinx>=1.5',          # For doc generation
        ],
        'dev': [
            'flake8>=3',            # For code style checking
            'pytest',               # For unit tests
            'pytest-cov',           # For coverage
            'codecov',              # For coverage
        ],
    },
)

