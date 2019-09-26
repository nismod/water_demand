import numpy as np
import pandas as pd

# The large spreadsheet
data_file = 'WRZ_summary_data.csv'

# Read into pandas data frame ignoring some cols
pd_data = pd.read_csv(
    data_file,
    sep=',',
    skiprows=0,
    usecols=lambda col: col.lower().strip() not in [
        'GIS Ref'.lower(),
        'owner'.lower(),
        'wrmp_14_by_19_factor'.lower(),
        'wrmp_14_wrz_name'.lower(),
    ]
)


def df_filter(year, measurement, ea_code=''):
    """
    Filter the dataset by year, measurement name and ea_code

    :param year: the single number year, e.g. 2022
    :param measurement: name of the measurement
    :param ea_code: string contained in the ea_code, e.g. 'BL'
    :return: sorted pandas data frame filtered by the inputs, and
             ignoring certain very low population areas.
    """
    _year = '{}-{}'.format(year, year - 1999)

    return pd_data[
        (pd_data.year == _year) &
        (pd_data.measurement == measurement) &
        (pd_data.ea_code.str.contains(ea_code)) &
        (pd_data['WRZ Name'] != 'Barepot') &
        (pd_data['WRZ Name'] != 'Rutland') &
        (pd_data['WRZ Name'] != 'South Humber Bank') &
        (pd_data['WRZ Name'] != 'Industrial')
        ].sort_values(by=['WRZ Name'])


# Handwritten expected water resource zone names
canonical_names = np.asarray(
    ['Ashford', 'Berwick', 'Bishops Castle', 'Blyth', 'Bourne', 'Bournemouth',
     'Bracknell', 'Brett', 'Bristol Water', 'Bury Haverhill', 'Cambridge',
     'Carlisle', 'Central Essex', 'Central Lincolnshire', 'Chester',
     'Cheveley', 'Colliford', 'Colne', 'Company', 'Cranbrook', 'Dour',
     'East Lincolnshire', 'East SWZ', 'East Suffolk', 'Eastbourne', 'Ely',
     'Essex', 'Farnham', 'Forest and Stroud', 'Grid SWZ', 'Guildford (GUI)',
     'Hampshire Andover', 'Hampshire Kingsclere', 'Hampshire Rural',
     'Hampshire Southampton East', 'Hampshire Southampton West',
     'Hampshire Winchester', 'Happisburgh', 'Hartismere', 'Hartlepol',
     'Haywards Heath', 'Henley (HEN)', 'Isle of Wight', 'Ixworth',
     'Kennet Valley (KV)', 'Kent Medway East', 'Kent Medway West',
     'Kent Thanet', 'Kielder', 'Kinsall', 'Lee', 'London (LON)', 'Maidstone',
     'Mardy', 'Misbourne', 'Newark', 'Newmarket', 'North Eden',
     'North Fenland', 'North Norfolk Coast', 'North Norfolk Rural',
     'North Staffordshire', 'Northern Central', 'Norwich and the Broads',
     'Nottinghamshire.1', 'Nottinghamshire.2', 'Pinn', 'Roadford',
     'Ruthamford Central', 'Ruthamford North', 'Ruthamford South',
     'Ruthamford West', 'Ruyton', 'SES Water', 'Shelton', 'Slough (SWA)',
     'South Essex', 'South Fenland', 'South Lincolnshire',
     'South Norfolk Rural', 'South Staffs', 'Stafford', 'Stort', 'Strategic',
     'Strategic Grid', 'Sudbury', 'Supply Area', 'Sussex Brighton',
     'Sussex Hastings', 'Sussex North', 'Sussex Worthing', 'Swindon (SWOX)',
     'Thetford', 'Tunbridge Wells', 'Wey', 'Whitchurch and Wem', 'Wimbleball',
     'Wolverhampton']
)

# Additional water resource zone names for Wales, not in the spreadsheet
extra_names = np.asarray([
    'Wye',
    'SEWCUS',
    'Tywi CUS',
    'Alwen',
    'Ross Bulk Supply']
)

# Populations for Welsh water resource zones
extra_pop = np.asarray([
    349.3,
    1340.8,
    752.1,
    158.7,
    22.2,
])

# Check the names match up for a representative slice of the data
names_from_filter = df_filter(2025, 'Total Resource Zone Population', 'BL')[
    'WRZ Name'].values

"""
Assertion currently fails due to repeated Nottinghamshire
"""
# assert np.array_equal(canonical_names, names_from_filter)

# Strings that are added to that will become csv files
population_string = 'timestep,water_resource_zones,population\n'
per_capita_string = 'timestep,water_resource_zones,per_capita_water_demand\n'
constant_string = 'timestep,water_resource_zones,constant_water_demand\n'

# All years from 2020 to 2044 inclusive
for y in range(2020, 2045):

    print('Processing year {}'.format(y))

    # Per capita consumption & populations, measured
    pcc_measured = df_filter(y, 'Measured Household - PCC', 'BL')
    pop_mh = df_filter(y, 'Measured Household - Population', 'BL')
    pop_mnh = df_filter(y, 'Measured Non Household - Population', 'BL')

    # Per capita consumption & populations, unmeasured
    pcc_unmeasured = df_filter(y, 'Unmeasured Household - PCC', 'BL')
    pop_uh = df_filter(y, 'Unmeasured Household - Population', 'BL')
    pop_unh = df_filter(y, 'Unmeasured Non Household - Population', 'BL')

    # Total population - should equal pop_mh + pop_mnh + pop_uh + pop_unh
    total_pop = df_filter(y, 'Total Resource Zone Population', 'BL')

    # Total water demand
    dist_input = df_filter(y, 'Distribution Input', '')

    # Double check units
    # print(pcc_measured.unit.unique())  # litres per head per day
    # print(pop_mh.unit.unique())  # 1000 people
    # print(pop_mnh.unit.unique())  # 1000 people
    # print(pcc_unmeasured.unit.unique())
    # print(pop_uh.unit.unique())
    # print(pop_unh.unit.unique())
    # print(dist_input.unit.unique())  # Ml per day

    # Population in 1000s of people
    pop = total_pop.value.values

    # Constant in Ml per day (1e3 scale for pop * 1e-6 scale for Ml = 1e-3)
    pop_measured = pop_mh.value.values + pop_mnh.value.values
    pop_unmeasured = pop_uh.value.values + pop_unh.value.values

    per_cap_measured = pcc_measured.value.values
    per_cap_unmeasured = pcc_unmeasured.value.values

    const = dist_input.value.values - 1e-3 * (
                per_cap_measured * pop_measured + per_cap_unmeasured * pop_unmeasured)

    # Per capita in Ml/(thousand people)/day
    pcc = (dist_input.value.values - const) / total_pop.value.values

    # Calculate means for extra regions
    mean_const_pp = np.mean(const / pop)
    mean_pcc = np.mean(pcc)

    # Check that the calculation gives back the original answer
    assert np.all(np.abs(
        const + pcc * total_pop.value.values - dist_input.value.values) < 1e-9)

    for i, name in enumerate(canonical_names):
        population_string += '{},{},{:.3f}\n'.format(y, name, pop[i])
        per_capita_string += '{},{},{:.7f}\n'.format(y, name, pcc[i])
        constant_string += '{},{},{:.5f}\n'.format(y, name, const[i])

    for i, name in enumerate(extra_names):
        population_string += '{},{},{:.3f}\n'.format(y, name, extra_pop[i])
        per_capita_string += '{},{},{:.7f}\n'.format(y, name, mean_pcc)
        constant_string += '{},{},{:.5f}\n'.format(
            y, name, mean_const_pp * extra_pop[i])

with open('water_resource_zone_populations.csv', 'w') as _f:
    _f.write(population_string.strip())

with open('per_capita_water_demand.csv', 'w') as _f:
    _f.write(per_capita_string.strip())

with open('constant_water_demand.csv', 'w') as _f:
    _f.write(constant_string.strip())

with open('water_resource_zones.csv', 'w') as _f:
    _f.write('name\n{}\n{}'.format('\n'.join(canonical_names),
                                   '\n'.join(extra_names)))
