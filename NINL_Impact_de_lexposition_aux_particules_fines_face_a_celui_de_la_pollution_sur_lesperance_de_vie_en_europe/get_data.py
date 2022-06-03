import pandas as pd

def clean_fine_particles():
    df = pd.read_csv("data/fine_particles_2008-2019_dirty.csv", sep=',', skipinitialspace=True,
                   quotechar='"', encoding='latin1')
    df.drop('AIRPOL', inplace=True, axis=1)
    df.drop(df[df.Value.str.contains(":")].index, inplace=True)
    df.drop(df[df.GEO.str.contains("Union européenne")].index, inplace=True)
    df.drop(df[(df['TIME'] < 2008) | (df['TIME'] > 2019)].index, inplace = True)    
    df.loc[ df.GEO.str.contains("Allemagne"), "GEO"] = "Allemagne"
    df = df.rename(columns={"TIME": "year", "GEO": "country", "Value": "value"})

    df.to_pickle("data/fine_particles_2008-2019.pkl")

def clean_lifespan():
    df = pd.read_csv("data/lifespan_2006-2020_dirty.csv", sep=',', skipinitialspace=True,
                   quotechar='"', encoding='latin1')
    df.drop('SEX', inplace=True, axis=1)
    df.drop('AGE', inplace=True, axis=1)
    df.drop('UNIT', inplace=True, axis=1)
    df.drop(df[df.Value.str.contains(":")].index, inplace=True)
    df.drop(df[(df['TIME'] < 2008) | (df['TIME'] > 2019)].index, inplace = True)    
    df = df.rename(columns={"TIME": "year", "GEO": "country", "Value": "value"})

    df.to_pickle("data/lifespan_2008-2019.pkl")

def clean_pollution():
    df = pd.read_csv("data/pollution_2008-2020_dirty.csv", sep=',', skipinitialspace=True,
                   quotechar='"', encoding='latin1')
    df.drop('HHTYP', inplace=True, axis=1)
    df.drop('INCGRP', inplace=True, axis=1)
    df.drop('UNIT', inplace=True, axis=1)
    df.drop(df[df.Value.str.contains(":")].index, inplace=True)
    df.drop(df[df.GEO.str.contains("Union européenne")].index, inplace=True)
    df.drop(df[df.GEO.str.contains("Zone euro")].index, inplace=True)
    df.drop(df[(df['TIME'] < 2008) | (df['TIME'] > 2019)].index, inplace = True)    
    df.loc[ df.GEO.str.contains("Allemagne"), "GEO"] = "Allemagne"
    df = df.rename(columns={"TIME": "year", "GEO": "country", "Value": "value"})

    df.to_pickle("data/pollution_2008-2019.pkl")

if __name__ == "__main__":
    clean_fine_particles()
    clean_lifespan()
    clean_pollution()