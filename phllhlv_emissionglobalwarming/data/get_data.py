import pandas as pd
from pathlib import Path

from pandas import DataFrame


def export_to_csv(df: DataFrame, path: str):
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)


def clean_temperature_world(temp_world: DataFrame):
    temp_world['dt'] = pd.to_datetime(temp_world['dt'])
    start_date = pd.to_datetime('1900-1-1')
    mask_world = temp_world['dt'] >= start_date
    temp_world_1900 = temp_world.loc[mask_world]
    temp_world_yearly = temp_world_1900.groupby([pd.Grouper(key='dt', freq='Y')])[
        'LandAverageTemperature'].mean().reset_index(name='Year')
    temp_world_yearly.rename(columns={'dt': 'Year', 'Year': 'AverageTemperature'}, inplace=True)
    temp_world_yearly['Year'] = pd.DatetimeIndex(temp_world_yearly['Year']).year
    temp_world_yearly['Country'] = 'World'
    return temp_world_yearly


def clean_temperature_country(temp_country: DataFrame):
    # Removing the duplicated countries and countries for which no information about the temperature
    temp_country_clean = DataFrame(temp_country[~temp_country['Country'].isin(
        ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands', 'United Kingdom', 'Africa', 'South America'])])
    temp_country_clean.replace(
        ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
        ['Denmark', 'France', 'Netherlands', 'United Kingdom'], inplace=True)

    temp_country_clean_copy = temp_country_clean.copy()
    temp_country_clean_copy['dt'] = pd.to_datetime(temp_country_clean['dt'])
    start_date = pd.to_datetime('1900-1-1')
    mask = temp_country_clean_copy['dt'] >= start_date
    temp_country_1900 = temp_country_clean_copy.loc[mask]
    temp_country_yearly = temp_country_1900.groupby([pd.Grouper(key='dt', freq='Y'), 'Country'])[
        'AverageTemperature'].mean().reset_index(name='Year')
    temp_country_yearly.rename(columns={'dt': 'Year', 'Year': 'AverageTemperature'}, inplace=True)
    temp_country_yearly['Year'] = pd.DatetimeIndex(temp_country_yearly['Year']).year
    return temp_country_yearly


def clean_temperature_data():
    temp_country = pd.read_csv('bad_global_land_temperatures_by_country.csv')
    temp_world = pd.read_csv('bad_global_temperatures_world.csv')
    temp_country_yearly = clean_temperature_country(temp_country)
    temp_world_yearly = clean_temperature_world(temp_world)
    final_temp_df = pd.concat([temp_world_yearly, temp_country_yearly], sort=True)
    final_temp_df.sort_values(['Year', 'Country'], inplace=True)
    final_temp_df.reset_index(inplace=True, drop=True)
    export_to_csv(final_temp_df, './clean/clean_global_land_temperature_by_country.csv')


def clean_emission_data():
    emission = pd.read_csv('bad_historical_emission_by_country.csv')
    # Calculate and add Mean values of emission of each industrial sectors of each country
    emission['Mean'] = emission.iloc[:, 5:34].mean(axis=1).round(decimals=3)
    # Get the total emission of all industrial sectors of each country
    total_emission = emission[emission['Sector'] == 'Total including LUCF']
    export_to_csv(total_emission, './clean/clean_mean_emission_by_country.csv')
    # Display by each year
    emission_countries_yearly = total_emission.melt(id_vars=["Country"], value_vars=total_emission.iloc[:, 5:34],
                                                    var_name="Year", value_name="TotalEmission")
    export_to_csv(emission_countries_yearly, './clean/clean_total_emission_by_country.csv')


if __name__ == '__main__':
    # clean emission data to desired dataframe structure
    clean_emission_data()
    # clean temperature data to desired dataframe structure
    clean_temperature_data()
