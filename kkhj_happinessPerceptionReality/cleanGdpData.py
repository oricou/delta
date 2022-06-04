import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# extract data
def get_dataframe():
    df = pd.read_csv("kkhj_happinessPerceptionReality/data/GDP_per_capita.csv")
    df.rename(columns={'Country Name': 'Country'}, inplace=True)
    df.drop("Indicator Name", inplace=True, axis=1)
    df.drop("Indicator Code", inplace=True, axis=1)
    first_year_to_drop = 1960
    last_year_to_drop = 2011
    for column_name in range(first_year_to_drop, last_year_to_drop + 1):
        df.drop(str(column_name), inplace=True, axis=1)
    df = df.melt(id_vars=["Country", "Country Code"],
                 var_name="Year",
                 value_name="Value")
    df = df.dropna(subset=['Value'])
    return df


def find_bin_idx_of_value(bins, value):
    array = np.asarray(value)
    idx = np.digitize(array, bins)
    return idx - 1


def area_before_val(counts, bins, val):
    right_bin_edge_index = find_bin_idx_of_value(bins, val)
    bin_width = np.diff(bins)[0]
    area = sum(bin_width * counts[:right_bin_edge_index])
    return area


def get_gdp_value_for_single_value(counts, bins, val, total_area):
    return area_before_val(counts, bins, val) / total_area * 10


# main function
def gdp_out_of_10():
    dataframe = get_dataframe()
    min_year = 2012
    max_year = 2020
    for year in range(min_year, max_year + 1):
        year_df = dataframe[dataframe['Year'] == str(year)]
        year_series = pd.Series(year_df['Value'])
        counts, bins, _ = plt.hist(year_series, bins=50, alpha=0.3, density=True, label="Data")
        total_area = sum(np.diff(bins) * counts)
        year_df = year_df.reset_index()
        for index, row in year_df.iterrows():
            location = row['Country']
            value = row['Value']
            gdp_value = get_gdp_value_for_single_value(counts, bins, value, total_area)
            dataframe.loc[(dataframe['Year'] == str(year)) & (dataframe['Country'] == location), ["GDP"]] = gdp_value
    return dataframe
