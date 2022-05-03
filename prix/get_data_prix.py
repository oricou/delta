import pandas as pd
import plotly

# Setting plotting backend to use plotly
pd.options.plotting.backend = "plotly"

def transform_df(df, pib):
    df = df.rename(columns = {"Location": "pays",
                              "SpatialDimValueCode": "code",
                              "Value": "prix"})
    
    # Keeping only needed columns
    df = df[['pays', 'code', 'prix']]
    df = df[df['prix'].notna()]
    df = pd.merge(df, pib, on = 'code')
    
    # Adding a new column ratio
    df['ratio'] = df.apply(lambda row: row.prix / row.pib * 100, axis=1)
    return df

def load_df():
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