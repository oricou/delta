import pandas as pd
import pycountry as pyc


# extract necessary columns and rows, get datasets ready for future instructions
def extract_education():
    df = pd.read_csv("kkhj_happinessPerceptionReality/data/educationLevel.csv")
    df.rename(columns={'TIME': 'Year'}, inplace=True)
    mask = (df['Year'] >= 2012) & (df['Year'] <= 2021)
    df = df[mask]
    df = (df.groupby(['LOCATION', 'Year'], as_index=False))["Value"].mean()
    df['LOCATION'] = df['LOCATION'].apply(lambda x: pyc.countries.get(alpha_3=x).name if pyc.countries.get(alpha_3=x) is not None else None)
    df.rename(columns={'LOCATION': 'Country'}, inplace=True)
    return df


# main function, convert data to index (out of 10)
def education_out_of_10():
    df = extract_education()
    df['Value'] = df['Value'].apply(lambda x: x/10)
    return df
