import pandas as pd
import numpy as np
import glob
import plotly.express as px
import os

# Pollution data
# --------------------------------------------------------------------------------------

pollution = pd.read_csv('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/pollution_2000_2021.csv',
                engine = 'python',
                parse_dates = True)
del pollution["Year"]
del pollution["Month"]
del pollution["Day"]
del pollution["Address"]
del pollution["County"]
del pollution["City"]
del pollution["O3 1st Max Value"]
del pollution["O3 1st Max Hour"]
del pollution["O3 AQI"]
del pollution["CO 1st Max Value"]
del pollution["CO 1st Max Hour"]
del pollution["CO AQI"]
del pollution["SO2 1st Max Value"]
del pollution["SO2 1st Max Hour"]
del pollution["SO2 AQI"]
del pollution["NO2 1st Max Value"]
del pollution["NO2 1st Max Hour"]
del pollution["NO2 AQI"]

# converting string dates to dates types
pollution['Date'] = pd.to_datetime(pollution['Date'], format='%Y-%m-%d')

# sort data by date
pollution = pollution.sort_values(['Date'])

# getting the mean of values at each date, ignoring the states where the data was taken from
pollution = pollution.resample('d', on='Date').mean()
pollution.rename(columns={'CO Mean': 'Concentration moyenne en CO'}, inplace=True)
pollution.rename(columns={'NO2 Mean': 'Concentration moyenne en NO2'}, inplace=True)
pollution.rename(columns={'O3 Mean': 'Concentration moyenne en O3'}, inplace=True)
pollution.rename(columns={'SO2 Mean': 'Concentration moyenne en SO2'}, inplace=True)

# saving dataframes
pollution.to_pickle("ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/pollution.pkl")

# Prices data
# --------------------------------------------------------------------------------------

prices = pd.read_csv('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/gas_price_US.csv',
                engine = 'python',
                parse_dates = True)

# converting string dates to dates types
prices['Date'] = pd.to_datetime(prices['Date'], format='%m/%d/%Y')

# removing dates too old
prices = prices.loc[(prices['Date'] >= '2000-01-03')]
prices.rename(columns={'Regular All Formulations Retail Gasoline Prices Dollars per Gallon': 'Prix moyen en dollar du gallon de gazole'}, inplace=True)

# saving dataframes
prices.to_pickle("ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/prices.pkl")

# Temperature and precipitation data
# --------------------------------------------------------------------------------------

path = 'ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/US_weather_data/'
filenames = glob.glob(path + "/*.csv")
cities = []

for f in filenames:
    df = pd.read_csv(f, engine = 'python', parse_dates = True)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.loc[(df['Date'] >= '2000-01-03')]
    df['Température moyenne en °C'] = (df[['tmax', 'tmin']].mean(axis=1) - 32)/1.8
    df['prcp'] = df['prcp']/2.54
    df.rename(columns={'prcp': 'Précipitation moyenne en cm'}, inplace=True)
    del df['tmax']
    del df['tmin']
    df = df.iloc[: , 1:]
    cities.append(df)

# averaging all cities data
average_cities = pd.concat(cities).groupby('Date', as_index=False).mean()

# saving dataframes
average_cities.to_pickle("ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/average_cities.pkl")
