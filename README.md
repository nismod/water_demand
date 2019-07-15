[![Build Status](https://dev.azure.com/OxfordRSE/Nismod2%20Water%20Demand/_apis/build/status/nismod.water_demand?branchName=master)](https://dev.azure.com/OxfordRSE/Nismod2%20Water%20Demand/_build/latest?definitionId=2&branchName=master)
[![codecov](https://codecov.io/gh/nismod/water_demand/branch/master/graph/badge.svg)](https://codecov.io/gh/nismod/water_demand)
![GitHub](https://img.shields.io/github/license/nismod/water_demand.svg?color=blue)
![Python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)

# A basic water demand model

A basic water demand model, where demand is a scalar multiple of population.

## Installation (user)
```
pip install git+https://github.com/nismod/water_demand.git@master#egg=water_demand
```

## Installation (developer)
```
git clone git@github.com:nismod/water_demand.git
pip install -e .[dev,docs]
```

## Basic usage

Create an instance of the `WaterDemand` class, constructing it with a sequence representing populations, a number or sequence representing the per capita water demand, and a number or sequence representing constant water demand.
The water demand is calculated as `constant + per_capita * population`.

### Global demand coefficients

```python
import water_demand
import numpy as np

# Define population (e.g. read from csv file)
pop = np.random.normal(size=20)

# Define the global per capita and constant demands
per_capita = 1.23
constant = 2.34

# Create the model
model = water_demand.WaterDemand(
    population=pop,
    per_capita_demand=per_capita,
    constant_demand=constant
)

# Simulate the water demand
demand = model.simulate()
```

### Local demand coefficients

```python
import water_demand
import numpy as np

# Define population (e.g. read from csv file)
pop = np.random.normal(size=20)

# Define local demand coefficients (e.g. read from csv files)
per_capita = np.random.normal(size=20)
constant = np.random.normal(size=20)

# Create the model
model = water_demand.WaterDemand(
    population=pop,
    per_capita_demand=per_capita,
    constant_demand=constant
)

# Simulate the water demand
demand = model.simulate()
```
