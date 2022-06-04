import numpy as np
import pandas as pd


def init_postal_code():
    postalCodes = pd.read_csv('https://bano.openstreetmap.fr/data/full.csv.gz', compression='gzip',
                              usecols=['01400', '46.147624', '4.923727'],
                              dtype={'01400': str, '46.147624': np.float64, '4.923727': np.float64})
    postalCodes.columns = ['Postal code', 'Latitude', 'Longitude']
    postalCodes['Latitude'] = postalCodes['Latitude'].apply(lambda lat: round(lat, 3))
    postalCodes['Longitude'] = postalCodes['Longitude'].apply(lambda long: round(long, 3))
    return postalCodes


def init_data_revenus():
    data_revenus = pd.read_excel('./bars/data/revenus_communes_2019.xlsx')  # header=3
    data_revenus.drop(data_revenus.columns[[0, 3, 7, 8, 9, 10, 11, 12, 13]], axis=1, inplace=True)
    data_revenus.drop(data_revenus.tail(2).index, inplace=True)  # drop last 2 rows
    data_revenus.rename(columns=lambda n: data_revenus[n][2], inplace=True)
    data_revenus.drop(index=[0, 1, 2], inplace=True)
    data_revenus = data_revenus[
        data_revenus["Revenu fiscal de référence par tranche (en euros)"].str.strip() == 'TOTAL']
    data_revenus = data_revenus[~data_revenus['Dép.'].str.startswith('B')]
    return data_revenus


def init_code_commune():
    code_commune = pd.read_csv('./bars/data/code-commune.csv', sep=';')
    code_commune.drop(['Nom_commune', 'Ligne_5', 'Libellé_d_acheminement', 'coordonnees_gps'], axis=1, inplace=True)
    code_commune.columns = ['Code commune', 'Postal code']
    code_commune['Postal code'] = code_commune['Postal code'].astype(str)
    code_commune['Postal code'] = code_commune['Postal code'].apply(
        lambda postalCode: '0' + postalCode if (len(postalCode) < 5) else postalCode).str.strip()
    return code_commune


def init_data_bars():
    data_bars = pd.read_csv('./bars/data/osm-fr-bars.csv', sep=';')
    data_bars = data_bars[["Geo Point", "Code postal", "Nom"]]
    data_bars.drop("Code postal", axis=1, inplace=True)

    latitudes = []
    longitudes = []
    for row in data_bars['Geo Point']:
        try:
            latitudes.append(row.split(',')[0])
            longitudes.append(row.split(',')[1])
        except:
            latitudes.append(np.NaN)
            longitudes.append(np.NaN)

    data_bars['Latitude'] = latitudes
    data_bars['Longitude'] = longitudes
    data_bars.drop('Geo Point', 1)

    data_bars.isnull().sum().sum()
    data_bars['Latitude'] = data_bars['Latitude'].astype(float)
    data_bars['Longitude'] = data_bars['Longitude'].astype(float)
    data_bars['Latitude'] = data_bars['Latitude'].apply(lambda lat: round(lat, 3))
    data_bars['Longitude'] = data_bars['Longitude'].apply(lambda long: round(long, 3))

    postalCodes = init_postal_code()
    data_bars = pd.merge(data_bars, postalCodes, how='left', on=['Latitude', 'Longitude']).drop_duplicates()
    data_bars["Postal code"] = data_bars["Postal code"].str.strip()
    data_bars.dropna(subset=['Postal code'], inplace=True)
    data_bars['Département'] = data_bars['Postal code'].apply(lambda code: str(code)[0:2])
    data_bars.drop_duplicates(subset=['Geo Point'], inplace=True)

    return data_bars


def init_barNumber():
    data_bars = init_data_bars()
    return data_bars.groupby(['Département'])['Département'].count().reset_index(name='Nombre de bars')


def update_data_revenus(data_revenus):
    code_commune = init_code_commune()

    data_revenus.insert(1, "Code commune", data_revenus['Dép.'].str.strip().apply(lambda dep: dep[:2]) + data_revenus['Commune'])
    data_revenus.drop(["Dép.", "Commune"], axis=1, inplace=True)
    data_revenus['Code commune'] = data_revenus['Code commune'].str.strip()
    data_revenus = pd.merge(data_revenus, code_commune, on=['Code commune'], how='left').drop(
        ['Revenu fiscal de référence par tranche (en euros)'], axis=1)
    data_revenus = data_revenus.drop_duplicates()
    data_revenus = data_revenus.reset_index(drop=True)
    return data_revenus


def init_data_bars_revenus(data_bars, data_revenus):
    data_bars_revenus = pd.merge(data_bars, update_data_revenus(data_revenus), on=['Postal code'], how='left')
    data_bars_revenus.drop(
        data_bars_revenus[data_bars_revenus['Revenu fiscal de référence des foyers fiscaux'] == 'n.c.'].index,
        inplace=True)
    data_bars_revenus.drop_duplicates(inplace=True)
    data_bars_revenus['Revenu fiscal de référence des foyers fiscaux'] = data_bars_revenus['Revenu fiscal de référence des foyers fiscaux'].astype(np.float64)
    data_bars_revenus['Revenu fiscal de référence par foyer fiscal'] = data_bars_revenus['Revenu fiscal de référence des foyers fiscaux'] / data_bars_revenus['Nombre de foyers fiscaux']
    return data_bars_revenus

def init_nbBar_revenu_byCp(data_bars_revenus):
    nbBar_revenu_byCp = pd.merge(
        data_bars_revenus.groupby('Postal code')['Revenu fiscal de référence par foyer fiscal'].mean().reset_index(),
        data_bars_revenus.groupby('Postal code')['Nom'].nunique().reset_index(), on=['Postal code'], how='inner')
    nbBar_revenu_byCp.columns = ['Postal code', 'Revenu fiscal de référence par foyer fiscal', 'Nombre de bars']
    return nbBar_revenu_byCp

def init_mean_by_bar_number(nbBar_revenu_byCp):
    mean_by_bar_number = nbBar_revenu_byCp.groupby('Nombre de bars').mean().reset_index()
    return mean_by_bar_number