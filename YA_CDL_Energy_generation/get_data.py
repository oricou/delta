import numpy as np
import pandas as pd
import pycountry_convert as pc

# Read data
data = pd.read_excel(
    'data/Data-file-Europe-Power-Sector-2020.xlsx', sheet_name='Data')
data = data.drop(columns=['Change on last year (%)',
                 'Change on last year (TWh)'])

# Transform dataframe for sunbursts plots
fossils = ['Coal', 'Hard Coal', 'Lignite', 'Gas', 'Other fossil', 'Nuclear']
renewables = ['Hydro', 'Wind', 'Solar', 'Bioenergy', 'Other renewables']
data['Kind of energy'] = data['Variable'].apply(
    lambda x: 'Renewable' if x in renewables else ('Fossil' if x in fossils else 'Other'))
data = data[data['Kind of energy'] != 'Other']

# Write dataframe in data/transformedData/sunburst_data.csv
data.to_csv('data/YA_CDL_Energy_generation/energy_per_source.csv')

# Create a new dataframe for the map and the line plot
energy_per_area_data = []
energy_sources = ['Coal', 'Hard Coal', 'Lignite', 'Gas',
                  'Nuclear', 'Hydro', 'Wind',
                  'Solar', 'Bioenergy']
areas = data['Area'].unique()

data_per_year = {str(year): data[data['Year'] == year]
                 for year in range(2000, 2021)}
for year in range(2000, 2021):
    for area in areas:
        tmp = data_per_year[str(
            year)][data_per_year[str(year)]['Area'] == area]
        total_generation = tmp.groupby('Area')['Generation (TWh)'].sum()
        group = tmp.groupby('Kind of energy')
        generation_per_kind = group['Generation (TWh)'].sum()

        total_energy_prod = tmp['Generation (TWh)'].sum()
        energy_sources_prod = [list(tmp[tmp['Variable'] == energy_source]['Generation (TWh)'])[
            0] for energy_source in energy_sources]
        energy_sources_share = [(energy_source_prod * 100 / total_energy_prod)
                                for energy_source_prod in energy_sources_prod]

        share_of_prod = generation_per_kind * 100 / total_energy_prod

        line = [year, area, total_generation[0], generation_per_kind['Fossil'],
                generation_per_kind['Renewable'], share_of_prod[0], share_of_prod[1]]
        line += energy_sources_prod + energy_sources_share
        energy_per_area_data.append(line)

columns = ['Year', 'Area', 'Total energy generation (TWh)', 'Fossil energy generation (TWh)', 'Renewable energy generation (TWh)',
           'Fossil energy share of generation (%)', 'Renewable energy share of generation (%)']
columns += [energy_source + ' generation (TWh)' for energy_source in energy_sources] + [
    energy_source + ' energy share of generation (%)' for energy_source in energy_sources]
energy_per_area = pd.DataFrame(data=energy_per_area_data, columns=columns)

# Add columns for the log scale
columns = energy_per_area.columns
for i in range(2, len(columns)):
    energy_per_area[columns[i] +
                    ' (log_10)'] = energy_per_area[columns[i]].apply(np.log10)

# Add iso_alpha3 column
energy_per_area['iso_alpha3'] = energy_per_area['Area'].apply(
    lambda x: pc.country_name_to_country_alpha3(x) if x != 'EU-27' and x != 'EU27+1' else x)

# Write dataframe in
energy_per_area.to_csv('data/YA_CDL_Energy_generation/energy_per_area.csv')
