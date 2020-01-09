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


### Data sources

Using 'Revised Draft Water Resources Management Plan 2019 Supply-Demand Data at Water Resource
Zone Level 2020/21 to 2044/45'

Provided by Environment Agency for research purposes (not shared publicly), last updated 09
August 2019. See related company level dataset published on
[gov.uk](https://data.gov.uk/dataset/fb38a40c-ebc1-4e6e-912c-bb47a76f6149/revised-draft-water-resources-management-plan-2019-supply-demand-data-at-company-level-2020-21-to-2044-45).

Relevant variables:

ea_code | measurement | unit
--- | --- | ---
11BL | Distribution input | Ml/d
11FP | Distribution Input | Ml/d
29BL | Measured Household - PCC | l/h/d
29FP | Measured Household - PCC | l/h/d
30BL | Unmeasured Household - PCC | l/h/d
30FP | Unmeasured Household - PCC | l/h/d
31BL | Average Household - PCC | l/h/d
31FP | Average Household - PCC | l/h/d
49BL | Measured Non Household - Population | 000's
49FP | Measured Non Household - Population | 000's
50BL | Unmeasured Non Household - Population | 000's
50FP | Unmeasured Non Household - Population | 000's
51BL | Measured Household - Population | 000's
51FP | Measured Household - Population | 000's
52BL | Unmeasured Household - Population | 000's
52FP | Unmeasured Household - Population | 000's
53BL | Total Resource Zone Population | 000's
53FP | Total Resource Zone Population | 000's

Note on scenarios:

>The baseline scenario (with BL suffix) represents 'business as usual'. This scenario reflects:
>
>- forecast changes to the amount of water available, through planned changes to abstraction
>  licences and through reductions to supply from climate change
>- continuation of current policies in demand management (including the committed leakage
>  levels, metering policies and implementation of companies’ water efficiency plans)
>- forecast changes to properties and population.
>
>For some companies, forecast demand exceeds the available supply over the planning period.
>Where this occurs, a water company must propose schemes (termed 'options') to increase
>supplies and/or reduce the demand for water.  Detailed option data is not included in this
>dataset because it commercially sensitive.
>
>The final planning scenario (with FP suffix) represents the company's forecast supply and
>demand as a result of the implementation of the additional supply and/or reduced demand
>options incorporated into its forecasts. This is the scenario that represents what a water
>company intends to doover the planning period to maintain the balance of supply and demand.

Section 1.3 *Scenarios explained* in [Water Resources Planning Components
Guide](https://data.gov.uk/dataset/fb38a40c-ebc1-4e6e-912c-bb47a76f6149/revised-draft-water-resources-management-plan-2019-supply-demand-data-at-company-level-2020-21-to-2044-45)


## Running in NISMOD

This model is integrated with population scenarios and a water supply model in
[nismod/nismod2](https://github.com/nismod/nismod2).

```bash
bash provision/get_data_water_demand.sh .
bash provision/install_water_demand.sh .
smif csv2parquet data/scenarios/water_demand/
smif run -b batch/arc_wd.batch -i local_binary
```
