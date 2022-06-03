import json
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import dateutil as du
import pandas as pd


def get_data_from_url(url, as_str):
    """Unzip the data and return the dataframe.

    :param url: url of the zip.
    :param as_str: columns to parse as string.
    :return:
    """
    data = urlopen(url)
    zipfile = ZipFile(BytesIO(data.read()))
    files = []
    with zipfile as f:
        for name in f.namelist():
            with f.open(name) as zd:
                files.append(
                    pd.read_csv(zd, delimiter=';', dtype={as_str: str}))
    return files[0]


def save_data_as_pkl(urlsn, urlsd):
    """Download online data and save it as pickle.

    :param urlsn: URL of naissance data.
    :param urlsd: URL of deces data.
    """
    dfn = get_data_from_url(urlsn, 'DEPNAIS')
    dfd = get_data_from_url(urlsd, 'DEPDEC')

    # Set 'date' from Month And Year information.
    dfn['date'] = dfn.apply(lambda x: convert_date(x.ANAIS, x.MNAIS), axis=1)
    dfn.set_index('date', inplace=True)

    # Set 'date' from Month And Year information.
    dfd['date'] = dfd.apply(lambda x: convert_date(x.ADEC, x.MDEC), axis=1)
    dfd['AGE'] = dfd['ADEC'] - dfd['ANAIS']
    dfd.set_index('date', inplace=True)

    # Get geojson department name.
    with open('data/jcwg_departements.geojson') as f:
        dep = json.load(f)

    # Create a map between department code and department name.
    dep_map = {d['properties']['code']: d['properties']['nom']
               for d in dep['features']}

    # Number of naissance/deces by department and date
    daten = dfn.groupby(['DEPNAIS', 'date']).size().rename(
        'SIZE').to_frame()
    dated = dfd.groupby(['DEPDEC', 'date']).size().rename(
        'SIZE').to_frame()

    # Number of naissance/deces by department
    depn = dfn.groupby('DEPNAIS').size().rename('SIZE').to_frame()
    depd = dfd.groupby('DEPDEC').size().rename('SIZE').to_frame()

    # Remove data about department not contained in the geojson
    depn['NAME'] = [dep_map[d]
                    if d in dep_map else 'NON'
                    for d in depn.index]
    depd['NAME'] = [dep_map[d]
                    if d in dep_map else 'NON'
                    for d in depd.index]

    depn = depn.drop(depn[depn['NAME'] == 'NON'].index)
    depd = depd.drop(depd[depd['NAME'] == 'NON'].index)

    # Data about naissance/deces of men/women by their age
    agemn = dfn.groupby(['DEPNAIS', 'AGEMERE']).size().rename('SIZEMEREN')
    agepn = dfn.groupby(['DEPNAIS', 'AGEPERE']).size().rename('SIZEPEREN')

    agemd = dfd.loc[dfd.SEXE == 2, ['DEPDEC', 'AGE']].groupby(
        ['DEPDEC', 'AGE']).size().rename('SIZEMERED')
    agepd = dfd.loc[dfd.SEXE == 1, ['DEPDEC', 'AGE']].groupby(
        ['DEPDEC', 'AGE']).size().rename('SIZEPERED')

    agen = pd.concat([agemn, agepn, ], axis=1)
    agen['SIZEMEREPEREN'] = agen['SIZEMEREN'] + agen[
        'SIZEPEREN']
    agen['MGMEREPEREN'] = (agen['SIZEMEREN'] + agen[
        'SIZEPEREN']) // 2

    aged = pd.concat([agemd, agepd, ], axis=1)
    aged['SIZEMEREPERED'] = aged['SIZEMERED'] + aged[
        'SIZEPERED']
    aged['MGMEREPERED'] = (aged['SIZEMERED'] + aged[
        'SIZEPERED']) // 2

    # Save to csv
    daten.fillna(0).to_pickle('data/jcwg_date_naissance.pkl')
    dated.fillna(0).to_pickle('data/jcwg_date_deces.pkl')

    depn.fillna(0).to_pickle('data/jcwg_department_naissance.pkl')
    depd.fillna(0).to_pickle('data/jcwg_department_deces.pkl')

    agen.fillna(0).to_pickle('data/jcwg_age_naissance.pkl')
    aged.fillna(0).to_pickle('data/jcwg_age_deces.pkl')


def convert_date(y, m):
    """Convert data to dataframe.datetime format.

    :param y: year.
    :param m: month.
    :return:
    """
    return du.parser.parse(f"15-{m}-{y}")


if __name__ == '__main__':
    save_data_as_pkl(
        'https://www.insee.fr/fr/statistiques/fichier/4768335/etatcivil2019_nais2019_csv.zip',
        'https://www.insee.fr/fr/statistiques/fichier/4801913/etatcivil2019_dec2019_csv.zip')
