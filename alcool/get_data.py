import pandas as pd
import urllib.request
import os
import numpy as np

# Specify the headers to be able to make request to GHO
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# Url of CSV https://apps.who.int/gho/data/node.resources.examples
urls = ['https://apps.who.int/gho/athena/api/GHO/SA_0000001413?format=csv',
        'https://apps.who.int/gho/athena/api/GHO/SA_0000001829?format=csv',
        'https://apps.who.int/gho/athena/api/GHO/SA_0000001830?format=csv',
        'https://apps.who.int/gho/athena/api/GHO/SA_0000001831?format=csv']

# Name of files who will be created
paths = ["gho_alcohol_consumer_past_12months.csv",
         "gho_average_price_500_mls_beer_in_us$.csv",
         "gho_average_price_500_mls_wine_in_us$.csv",
         "gho_average_price_500_mls_spirits_in_us$.csv"]
path_csv_country = 'country_code.csv'

main_data_folder = "./data/"
data_folder = "./alcool/data/"

# Create a csv with the code alpha-3 asociated to each country
def get_country_name():
    fields=['name', 'alpha-3']
    cols=['pays', 'code']

    df_country = pd.read_csv('https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv',
                            usecols=fields)

    df_country.columns = cols

    df_country.to_csv(main_data_folder + path_csv_country, index=False)
    df_country.to_csv(data_folder + path_csv_country, index=False)

if __name__ == "alcool.get_data":

    if not os.path.isfile(main_data_folder + path_csv_country) or \
    not os.path.isfile(data_folder + path_csv_country):
        get_country_name()

    for i in range(len(paths)):
        path, url = paths[i], urls[i]

        if not os.path.isfile(data_folder + path):
            urllib.request.urlretrieve(url, data_folder + path)

        if not os.path.isfile(main_data_folder + path):
            urllib.request.urlretrieve(url, main_data_folder + path)

def compute_mean(df, pays):
        return np.mean([df.loc[(df.pays == pays) & (df.sexe == 'MLE')].values[0][1],
                        df.loc[(df.pays == pays) & (df.sexe == 'FMLE')].values[0][1]])

def load_df_cons():
    df_country = pd.read_csv('data/country_code.csv')
    alcohol_consumption = pd.read_csv('data/gho_alcohol_consumer_past_12months.csv')

    # Removing rows with missing values
    alcohol_consumption.dropna(how='all', axis=1, inplace=True)

    # Renaming columns
    alcohol_consumption = alcohol_consumption.rename(columns = {"COUNTRY": "code",
                                                                "Display Value": "pourcentage",
                                                                "SEX": "sexe",
                                                                "REGION": "region"})

    alcohol_consumption = alcohol_consumption[['code', 'pourcentage', 'sexe', 'region']]
    alcohol_consumption = pd.merge(alcohol_consumption, df_country[['code','pays']],on='code', how='left')

    pib = pd.read_csv('data/gdp-per-capita-worldbank.csv')

    # Removing rows with missing values
    pib.dropna(how='all', axis=1, inplace=True)

    # Renaming columns
    pib = pib.rename(columns = {"GDP per capita, PPP (constant 2017 international $)": "pib",
                                "Year": "annee",
                                "Code": "code"})
    del pib['Entity']

    # Keeping rows with values
    alcohol_consumption = alcohol_consumption.loc[alcohol_consumption["pourcentage"] != '.']

    # Casting value to float
    alcohol_consumption = alcohol_consumption.astype({"pourcentage" : "float64"})

    
    alcohol_consumption['pourcentage'] = alcohol_consumption.apply(lambda row: compute_mean(alcohol_consumption, row.pays) if row.sexe == "BTSX" 
                                                                        else row.pourcentage, axis=1)

    # Merging alcohol consumption and pib dataframes on code
    df = pd.merge(alcohol_consumption, pib, on = 'code')

    # Removing code column
    del df['code']

    # Sorting by years
    df = df.sort_values(by = ['annee'])


    return df

def transform_df(df, pib):
    df_country = pd.read_csv('data/country_code.csv')

    df.dropna(how='all', axis=1, inplace=True)
    df = df.rename(columns = {"COUNTRY": "code",
                              "Display Value": "prix"})
    
    df = pd.merge(df, df_country[['code','pays']],on='code', how='left')
    
    # Keeping only needed columns
    df = df[['pays', 'code', 'prix']]
    df = df[df['prix'].notna()]
    df = pd.merge(df, pib, on = 'code')
    
    # Adding a new column ratio
    df['ratio'] = df.apply(lambda row: row.prix / row.pib * 100, axis=1)
    return df

def load_df_prix():
    pib = pd.read_csv('data/gdp-per-capita-worldbank.csv')

    # Removing rows with missing values
    pib.dropna(how='all', axis=1, inplace=True)

    # Renaming columns
    pib = pib.rename(columns = {"GDP per capita, PPP (constant 2017 international $)": "pib",
                                "Year": "annee",
                                "Code": "code"})
    
    pib = pib.sort_values(by = ['annee'])
    pib = pib.drop_duplicates(subset=['code'], keep='last')

    df_beer = pd.read_csv('data/gho_average_price_500_mls_beer_in_us$.csv')
    df_beer = transform_df(df_beer, pib)

    df_wine = pd.read_csv('data/gho_average_price_500_mls_wine_in_us$.csv')
    df_wine = transform_df(df_wine, pib)

    df_spirits = pd.read_csv('data/gho_average_price_500_mls_spirits_in_us$.csv')
    df_spirits = transform_df(df_spirits, pib)
    
    return df_beer, df_wine, df_spirits