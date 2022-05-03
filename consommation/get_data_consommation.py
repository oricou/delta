import pandas as pd
import plotly

# Setting plotting backend to use plotly
pd.options.plotting.backend = "plotly"

def load_df():
    alcohol_consumption = pd.read_csv('data/gho_alcohol_consumer_past_12months.csv')

    # Removing rows with missing values
    alcohol_consumption.dropna(how='all', axis=1, inplace=True)

    # Renaming columns
    alcohol_consumption = alcohol_consumption.rename(columns = {"SpatialDimValueCode": "code",
                                                                "Location": "pays",
                                                                "Value": "pourcentage",
                                                                "Dim1ValueCode": "sexe",
                                                                "ParentLocationCode": "region"})

    pib = pd.read_csv('data/gdp-per-capita-worldbank.csv')

    # Renaming columns
    pib = pib.rename(columns = {"GDP per capita, PPP (constant 2017 international $)": "pib",
                                "Year": "annee",
                                "Code": "code"})
    del pib['Entity']

    # Keeping rows with vlaues
    alcohol_consumption = alcohol_consumption.loc[alcohol_consumption["pourcentage"] != '.']

    # Casting value to float
    alcohol_consumption = alcohol_consumption.astype({"pourcentage" : "float64"})

    # Merging alcohol consumption and pib dataframes on code
    df = pd.merge(alcohol_consumption, pib, on = 'code')

    # Removing code column
    del df['code']

    # Sorting by years
    df = df.sort_values(by = ['annee'])

    return df