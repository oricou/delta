import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import gzip
import os
import pickle
from datetime import datetime
from multiprocessing import Pool, freeze_support




def downloadMissingFiles(station_df, path='data/daily_stations/'):
    '''
    Télécharge les relevés météos des stations dont le nom est présent dans
    'station_df' si ils ne sont pas présent en local
    '''
    missing = 0
    url = ' https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/'
    print('missing file : ')
    for s in station_df['Station ID']: # Parcours le dataframe par ID
        if not os.path.exists(path + s + '.csv'): #regarde si le fichier existe déja en local
            missing += 1
            r = requests.get(url + s + '.csv.gz', allow_redirects=True) #demande le fichier au site
            f = gzip.decompress(r.content) #décompresse le fichier
            open(path + s + '.csv' , 'wb').write(f) #sauvegarde le fichier sous forme de csv
            print(s, ', ', end = '')
    print('\n', missing , 'files were missing') 


def downloadSingleFile(file_name, path='data/daily_stations/'):
    '''
    Télécharge un fichier si il n'existe pas en local
    '''

    url = ' https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/'
    if not os.path.exists(path + file_name + '.csv'):
        r = requests.get(url + file_name + '.csv.gz', allow_redirects=True) #demande le fichier au site
        f = gzip.decompress(r.content) #décompresse le fichier
        open(path + file_name + '.csv' , 'wb').write(f) #sauvegarde le fichier sous forme de csv
        print(file_name, " downloaded")



