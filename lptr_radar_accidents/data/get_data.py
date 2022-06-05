import datetime
import dateutil as du
import glob
import json
import numpy as np
import pandas as pd
import pathlib
import re
import requests
import sys

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

# we use data.gouv.fr API
url_accidents = "https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/"
accidents_ressource = [
    {"sep" : ',' ,"date" : 2005 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20160913-155958/caracteristiques_2005.csv"},
    {"sep" : ',' ,"date" : 2006 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20160909-180009/caracteristiques_2006.csv"},
    {"sep" : ',' ,"date" : 2007 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20160909-180642/caracteristiques_2007.csv"},
    {"sep" : ',' ,"date" : 2008 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20160909-180939/caracteristiques_2008.csv"},
    {"sep" : '\t' ,"date" : 2009 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20160422-111851/caracteristiques_2009.csv"},
    {"sep" : ',' ,"date" : 2010 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation-sur-6-annees/20150806-155035/caracteristiques_2010.csv"},
    {"sep" : ',' ,"date" : 2011 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation-sur-6-annees/20150806-154723/caracteristiques_2011.csv"},
    {"sep" : ',' ,"date" : 2012 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation-sur-6-annees/20150806-154431/caracteristiques_2012.csv"},
    {"sep" : ',' ,"date" : 2013 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation-sur-6-annees/20150806-154105/caracteristiques_2013.csv"},
    {"sep" : ',' ,"date" : 2014 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation-sur-6-annees/20150806-153701/caracteristiques_2014.csv"},
    {"sep" : ',' ,"date" : 2015 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20160909-181230/caracteristiques_2015.csv"},
    {"sep" : ',' ,"date" : 2016 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20170915-153739/caracteristiques_2016.csv"},
    {"sep" : ',' ,"date" : 2017 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20180927-111012/caracteristiques-2017.csv"},
    {"sep" : ',' ,"date" : 2018 , "url" : "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20191014-111741/caracteristiques-2018.csv"},
]
url_radars = "https://static.data.gouv.fr/resources/radars-automatiques/20181025-141231/radars.csv"

def prepare_accidents():
    # Download
    accidents = {}
    dtype = {'lat':str,'long':str,'an':int, 'dep':int}
    for ressource in accidents_ressource:
        accidents[ressource['date']] = pd.read_csv(ressource['url'], encoding='latin',
            on_bad_lines='skip',sep=ressource['sep'], dtype=dtype)
    df = pd.concat(accidents)

    # Processing
    df.loc[df['an'] < 2000,'an'] += 2000

    def convert_dep(x):
        if x % 10 == 0:
            x =  x / 10
        return int(x)

    df['dep'] = df['dep'].apply(convert_dep).astype(str)
    df = df[(df['long']=='-') == False]
    def convert_deg(x):
        if not isinstance(x, str) or x == '-':
            return np.nan
        return float(x[:2]+'.'+ x[2:])

    df.loc[:,'long'] = df['long'].apply(convert_deg)
    df.loc[:,'lat'] = df['lat'].apply(convert_deg)

    df = df[["an", "adr", "lat", "long","Num_Acc", "dep"]]

    # Saving
    return df

def prepare_radars():
    # Download
    df2 = pd.read_csv(url_radars)

    # Processing
    df2["an"] = pd.DatetimeIndex(df2['date_installation']).year
    outlier = df2.departement.unique()[-1]
    df2 = df2.loc[df2['departement'] != outlier]

    radars_year = df2[["an", "emplacement", "latitude", "longitude", "id", "departement"]].copy()
    radars_year = radars_year.rename(columns=
        {"latitude":"lat", "longitude":"long","departement":"dep"}).copy()

    return radars_year

def prepare_data():
    radar_year = prepare_radars()
    radar_year.to_pickle("lptr_radars.pkl")

    df = prepare_accidents()
    df_small = df[df['lat'] > 30]
    df_small = df_small.dropna().copy()
    df_small.to_pickle("lptr_accidents.pkl")

    df = df.groupby(["dep","an"]).count().drop(columns=["long","lat","adr"])
    radar_year = radar_year.groupby(["dep","an"]).count().drop(columns=["long","lat","emplacement"])

    merge = df.merge(radar_year, on=["dep","an"])
    merge = merge.reset_index().rename(columns={"Num_Acc":"nb d'accidents","id":"nb de radars"})
    merge['nb de radars'] = merge['nb de radars'].cumsum()
    merge.to_pickle("lptr_radar_accidents_dep.pkl")



if __name__ == '__main__':
    prepare_data()