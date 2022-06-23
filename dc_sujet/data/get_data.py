import pandas as pd
import numpy as np

url = 'https://www.data.gouv.fr/fr/datasets/r/5c4e1452-3850-4b59-b11c-3dd51d7fb8b5'
df = pd.read_csv(url, dtype={'dep': 'str'})

df = df.set_index(['dep', 'date']).sort_index()

df = df.drop(['R', 'cv_dose1', 'rad', 'incid_rad'], axis=1)

# Set tx_pos NaN to mean
x = df.reset_index()['tx_pos'].mean()
df['tx_pos'].fillna(x, inplace=True)


# Set tx_incid NaN to mean
x = df.reset_index()['tx_incid'].mean()
df['tx_incid'].fillna(x, inplace=True)


df['pos'].fillna(0, inplace=True)

x = df.reset_index()['pos_7j'].mean()
df['pos_7j'].fillna(x, inplace=True)


columns = ['incid_hosp', 'incid_rea', 'incid_dchosp', 'reg_incid_rea']
df[columns] = df[columns].fillna(0)

df.to_pickle('covid-all-stats-departments.pkl')
