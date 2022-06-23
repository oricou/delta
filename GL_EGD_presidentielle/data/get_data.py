import numpy as np
import pandas as pd


def get_sondage_tour_1():
    df = pd.read_csv('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv')
    df.drop(['id', 'echantillon', 'erreur_sup', 'sous_echantillon', 'commanditaire',
             'erreur_inf', 'population', 'rolling', 'media', 'parti'], axis=1, inplace=True)
    df = df[df['nom_institut'] == 'Ipsos']
    df["hypothese"].replace(np.nan, "tous", inplace=True)
    df = df[(df['hypothese'] == "tous") & (df['tour'] == "Premier tour")]
    df.reset_index()
    df['date_enquete'] = pd.to_datetime(df['fin_enquete'])
    df = df[df['tour'] == "Premier tour"]
    df = df.sort_values(by="date_enquete")
    df.to_csv('sondages_tour_1.csv')


def get_sondage_tour_2():
    df = pd.read_csv('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv')

    df.drop(['parti', 'id', 'commanditaire', 'debut_enquete', 'population', 'rolling', 'media', 'sous_echantillon'],
            axis=1, inplace=True)
    df = df[df['tour'] == "Deuxième tour"]
    df.replace("Hypothèse Macron", "Hypothèse Macron / Le Pen", inplace=True)
    df.replace("Hypothèse Le Pen / Macron", "Hypothèse Macron / Le Pen", inplace=True)
    df.replace(np.nan, "Hypothèse Macron / Le Pen", inplace=True)
    df.reset_index(inplace=True)
    df = df[df["hypothese"] == "Hypothèse Macron / Le Pen"]
    df['date_enquete'] = pd.to_datetime(df['fin_enquete'])
    df_ifop = df[df['nom_institut'] == 'Ifop']
    df_ifop = df_ifop.sort_values(by="date_enquete")
    df_ifop.to_csv('sondages_tour_2.csv')


def get_tdp_dupont():
    df_pt1_dupont = pd.read_csv("dupont/premier_tour_1_dupont.csv", sep=";").fillna(0)
    df_pt2_dupont = pd.read_csv("dupont/premier_tour_2_dupont.csv", sep=";").fillna(0)
    df_sp1_dupont = pd.read_csv("dupont/seconde_periode_1_dupont.csv", sep=";").fillna(0)
    df_sp2_dupont = pd.read_csv("dupont/seconde_periode_2_dupont.csv", sep=";").fillna(0)
    df_sp3_dupont = pd.read_csv("dupont/seconde_periode_3_dupont.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_dupont = df_pt1_dupont[df_pt1_dupont['Candidat'] == type]
    df_pt2_dupont = df_pt2_dupont[df_pt2_dupont['Candidat'] == type]
    df_sp1_dupont = df_sp1_dupont[df_sp1_dupont['Candidat'] == type]
    df_sp2_dupont = df_sp2_dupont[df_sp2_dupont['Candidat'] == type]
    df_sp3_dupont = df_sp3_dupont[df_sp3_dupont['Candidat'] == type]

    df_pt1_dupont.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_dupont.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_dupont.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_dupont.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_dupont.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_dupont.columns[2:]:
        df_pt1_dupont[col] = pd.to_timedelta(df_pt1_dupont[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_dupont[col] = pd.to_timedelta(df_pt2_dupont[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_dupont[col] = pd.to_timedelta(df_sp1_dupont[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_dupont[col] = pd.to_timedelta(df_sp2_dupont[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_dupont[col] = pd.to_timedelta(df_sp3_dupont[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_dupont["Période"] = "13/03/2022"
    df_sp2_dupont["Période"] = "20/03/2022"
    df_sp3_dupont["Période"] = "27/03/2022"
    df_pt1_dupont["Période"] = "03/04/2022"
    df_pt2_dupont["Période"] = "08/04/2022"

    df_pt1_dupont["Somme"] = (
            df_pt1_dupont['Tranche (6h-9h)(durée)'] + df_pt1_dupont['Tranche (6h-9h)(durée)'] + df_pt1_dupont[
        'Tranche (9h-18h)(durée)'] + df_pt1_dupont['Tranche (18h-24h)(durée)'])

    df_pt2_dupont["Somme"] = (df_pt2_dupont['Tranche (6h-9h)(durée)'] + df_pt2_dupont['Tranche (6h-9h)(durée)'] +
                              df_pt2_dupont['Tranche (9h-18h)(durée)'] + df_pt2_dupont['Tranche (18h-24h)(durée)'])

    df_sp1_dupont["Somme"] = (df_sp1_dupont['Tranche (6h-9h)(durée)'] + df_sp1_dupont['Tranche (6h-9h)(durée)'] +
                              df_sp1_dupont['Tranche (9h-18h)(durée)'] + df_sp1_dupont['Tranche (18h-24h)(durée)'])

    df_sp2_dupont["Somme"] = (df_sp2_dupont['Tranche (6h-9h)(durée)'] + df_sp2_dupont['Tranche (6h-9h)(durée)'] +
                              df_sp2_dupont['Tranche (9h-18h)(durée)'] + df_sp2_dupont['Tranche (18h-24h)(durée)'])

    df_sp3_dupont["Somme"] = (df_sp3_dupont['Tranche (6h-9h)(durée)'] + df_sp3_dupont['Tranche (6h-9h)(durée)'] +
                              df_sp3_dupont['Tranche (9h-18h)(durée)'] + df_sp3_dupont['Tranche (18h-24h)(durée)'])

    df_sp1_dupont['Période'] = pd.to_datetime(df_sp1_dupont['Période'], dayfirst=True)
    df_sp2_dupont['Période'] = pd.to_datetime(df_sp2_dupont['Période'], dayfirst=True)
    df_sp3_dupont['Période'] = pd.to_datetime(df_sp3_dupont['Période'], dayfirst=True)
    df_pt1_dupont['Période'] = pd.to_datetime(df_pt1_dupont['Période'], dayfirst=True)
    df_pt2_dupont['Période'] = pd.to_datetime(df_pt2_dupont['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_dupont = pd.concat([df_sp1_dupont[l], df_sp2_dupont[l], df_sp3_dupont[l], df_pt1_dupont[l], df_pt2_dupont[l]])
    return df_dupont


def get_tdp_arthaud():
    df_pt1_arthaud = pd.read_csv("arthaud/premier_tour_1_arthaud.csv", sep=";").fillna(0)
    df_pt2_arthaud = pd.read_csv("arthaud/premier_tour_2_arthaud.csv", sep=";").fillna(0)
    df_sp1_arthaud = pd.read_csv("arthaud/seconde_periode_1_arthaud.csv", sep=";").fillna(0)
    df_sp2_arthaud = pd.read_csv("arthaud/seconde_periode_2_arthaud.csv", sep=";").fillna(0)
    df_sp3_arthaud = pd.read_csv("arthaud/seconde_periode_3_arthaud.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_arthaud = df_pt1_arthaud[df_pt1_arthaud['Candidat'] == type]
    df_pt2_arthaud = df_pt2_arthaud[df_pt2_arthaud['Candidat'] == type]
    df_sp1_arthaud = df_sp1_arthaud[df_sp1_arthaud['Candidat'] == type]
    df_sp2_arthaud = df_sp2_arthaud[df_sp2_arthaud['Candidat'] == type]
    df_sp3_arthaud = df_sp3_arthaud[df_sp3_arthaud['Candidat'] == type]

    df_pt1_arthaud.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_arthaud.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_arthaud.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_arthaud.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_arthaud.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_arthaud.columns[2:]:
        df_pt1_arthaud[col] = pd.to_timedelta(df_pt1_arthaud[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_arthaud[col] = pd.to_timedelta(df_pt2_arthaud[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_arthaud[col] = pd.to_timedelta(df_sp1_arthaud[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_arthaud[col] = pd.to_timedelta(df_sp2_arthaud[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_arthaud[col] = pd.to_timedelta(df_sp3_arthaud[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_arthaud["Période"] = "13/03/2022"
    df_sp2_arthaud["Période"] = "20/03/2022"
    df_sp3_arthaud["Période"] = "27/03/2022"
    df_pt1_arthaud["Période"] = "03/04/2022"
    df_pt2_arthaud["Période"] = "08/04/2022"

    df_pt1_arthaud["Somme"] = (
            df_pt1_arthaud['Tranche (6h-9h)(durée)'] + df_pt1_arthaud['Tranche (6h-9h)(durée)'] + df_pt1_arthaud[
        'Tranche (9h-18h)(durée)'] + df_pt1_arthaud['Tranche (18h-24h)(durée)'])

    df_pt2_arthaud["Somme"] = (df_pt2_arthaud['Tranche (6h-9h)(durée)'] + df_pt2_arthaud['Tranche (6h-9h)(durée)'] +
                               df_pt2_arthaud['Tranche (9h-18h)(durée)'] + df_pt2_arthaud['Tranche (18h-24h)(durée)'])

    df_sp1_arthaud["Somme"] = (df_sp1_arthaud['Tranche (6h-9h)(durée)'] + df_sp1_arthaud['Tranche (6h-9h)(durée)'] +
                               df_sp1_arthaud['Tranche (9h-18h)(durée)'] + df_sp1_arthaud['Tranche (18h-24h)(durée)'])

    df_sp2_arthaud["Somme"] = (df_sp2_arthaud['Tranche (6h-9h)(durée)'] + df_sp2_arthaud['Tranche (6h-9h)(durée)'] +
                               df_sp2_arthaud['Tranche (9h-18h)(durée)'] + df_sp2_arthaud['Tranche (18h-24h)(durée)'])

    df_sp3_arthaud["Somme"] = (df_sp3_arthaud['Tranche (6h-9h)(durée)'] + df_sp3_arthaud['Tranche (6h-9h)(durée)'] +
                               df_sp3_arthaud['Tranche (9h-18h)(durée)'] + df_sp3_arthaud['Tranche (18h-24h)(durée)'])

    df_sp1_arthaud['Période'] = pd.to_datetime(df_sp1_arthaud['Période'], dayfirst=True)
    df_sp2_arthaud['Période'] = pd.to_datetime(df_sp2_arthaud['Période'], dayfirst=True)
    df_sp3_arthaud['Période'] = pd.to_datetime(df_sp3_arthaud['Période'], dayfirst=True)
    df_pt1_arthaud['Période'] = pd.to_datetime(df_pt1_arthaud['Période'], dayfirst=True)
    df_pt2_arthaud['Période'] = pd.to_datetime(df_pt2_arthaud['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_arthaud = pd.concat(
        [df_sp1_arthaud[l], df_sp2_arthaud[l], df_sp3_arthaud[l], df_pt1_arthaud[l], df_pt2_arthaud[l]])
    return df_arthaud


def get_tdp_hidalgo():
    df_pt1_hidalgo = pd.read_csv("hidalgo/premier_tour_1_hidalgo.csv", sep=";").fillna(0)
    df_pt2_hidalgo = pd.read_csv("hidalgo/premier_tour_2_hidalgo.csv", sep=";").fillna(0)
    df_sp1_hidalgo = pd.read_csv("hidalgo/seconde_periode_1_hidalgo.csv", sep=";").fillna(0)
    df_sp2_hidalgo = pd.read_csv("hidalgo/seconde_periode_2_hidalgo.csv", sep=";").fillna(0)
    df_sp3_hidalgo = pd.read_csv("hidalgo/seconde_periode_3_hidalgo.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_hidalgo = df_pt1_hidalgo[df_pt1_hidalgo['Candidat'] == type]
    df_pt2_hidalgo = df_pt2_hidalgo[df_pt2_hidalgo['Candidat'] == type]
    df_sp1_hidalgo = df_sp1_hidalgo[df_sp1_hidalgo['Candidat'] == type]
    df_sp2_hidalgo = df_sp2_hidalgo[df_sp2_hidalgo['Candidat'] == type]
    df_sp3_hidalgo = df_sp3_hidalgo[df_sp3_hidalgo['Candidat'] == type]

    df_pt1_hidalgo.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_hidalgo.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_hidalgo.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_hidalgo.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_hidalgo.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_hidalgo.columns[2:]:
        df_pt1_hidalgo[col] = pd.to_timedelta(df_pt1_hidalgo[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_hidalgo[col] = pd.to_timedelta(df_pt2_hidalgo[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_hidalgo[col] = pd.to_timedelta(df_sp1_hidalgo[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_hidalgo[col] = pd.to_timedelta(df_sp2_hidalgo[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_hidalgo[col] = pd.to_timedelta(df_sp3_hidalgo[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_hidalgo["Période"] = "13/03/2022"
    df_sp2_hidalgo["Période"] = "20/03/2022"
    df_sp3_hidalgo["Période"] = "27/03/2022"
    df_pt1_hidalgo["Période"] = "03/04/2022"
    df_pt2_hidalgo["Période"] = "08/04/2022"

    df_pt1_hidalgo["Somme"] = (
            df_pt1_hidalgo['Tranche (6h-9h)(durée)'] + df_pt1_hidalgo['Tranche (6h-9h)(durée)'] + df_pt1_hidalgo[
        'Tranche (9h-18h)(durée)'] + df_pt1_hidalgo['Tranche (18h-24h)(durée)'])

    df_pt2_hidalgo["Somme"] = (df_pt2_hidalgo['Tranche (6h-9h)(durée)'] + df_pt2_hidalgo['Tranche (6h-9h)(durée)'] +
                               df_pt2_hidalgo['Tranche (9h-18h)(durée)'] + df_pt2_hidalgo['Tranche (18h-24h)(durée)'])

    df_sp1_hidalgo["Somme"] = (df_sp1_hidalgo['Tranche (6h-9h)(durée)'] + df_sp1_hidalgo['Tranche (6h-9h)(durée)'] +
                               df_sp1_hidalgo['Tranche (9h-18h)(durée)'] + df_sp1_hidalgo['Tranche (18h-24h)(durée)'])

    df_sp2_hidalgo["Somme"] = (df_sp2_hidalgo['Tranche (6h-9h)(durée)'] + df_sp2_hidalgo['Tranche (6h-9h)(durée)'] +
                               df_sp2_hidalgo['Tranche (9h-18h)(durée)'] + df_sp2_hidalgo['Tranche (18h-24h)(durée)'])

    df_sp3_hidalgo["Somme"] = (df_sp3_hidalgo['Tranche (6h-9h)(durée)'] + df_sp3_hidalgo['Tranche (6h-9h)(durée)'] +
                               df_sp3_hidalgo['Tranche (9h-18h)(durée)'] + df_sp3_hidalgo['Tranche (18h-24h)(durée)'])

    df_sp1_hidalgo['Période'] = pd.to_datetime(df_sp1_hidalgo['Période'], dayfirst=True)
    df_sp2_hidalgo['Période'] = pd.to_datetime(df_sp2_hidalgo['Période'], dayfirst=True)
    df_sp3_hidalgo['Période'] = pd.to_datetime(df_sp3_hidalgo['Période'], dayfirst=True)
    df_pt1_hidalgo['Période'] = pd.to_datetime(df_pt1_hidalgo['Période'], dayfirst=True)
    df_pt2_hidalgo['Période'] = pd.to_datetime(df_pt2_hidalgo['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_hidalgo = pd.concat(
        [df_sp1_hidalgo[l], df_sp2_hidalgo[l], df_sp3_hidalgo[l], df_pt1_hidalgo[l], df_pt2_hidalgo[l]])
    return df_hidalgo


def get_tdp_jadot():
    df_pt1_jadot = pd.read_csv("jadot/premier_tour_1_jadot.csv", sep=";").fillna(0)
    df_pt2_jadot = pd.read_csv("jadot/premier_tour_2_jadot.csv", sep=";").fillna(0)
    df_sp1_jadot = pd.read_csv("jadot/seconde_periode_1_jadot.csv", sep=";").fillna(0)
    df_sp2_jadot = pd.read_csv("jadot/seconde_periode_2_jadot.csv", sep=";").fillna(0)
    df_sp3_jadot = pd.read_csv("jadot/seconde_periode_3_jadot.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_jadot = df_pt1_jadot[df_pt1_jadot['Candidat'] == type]
    df_pt2_jadot = df_pt2_jadot[df_pt2_jadot['Candidat'] == type]
    df_sp1_jadot = df_sp1_jadot[df_sp1_jadot['Candidat'] == type]
    df_sp2_jadot = df_sp2_jadot[df_sp2_jadot['Candidat'] == type]
    df_sp3_jadot = df_sp3_jadot[df_sp3_jadot['Candidat'] == type]

    df_pt1_jadot.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_jadot.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_jadot.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_jadot.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_jadot.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_jadot.columns[2:]:
        df_pt1_jadot[col] = pd.to_timedelta(df_pt1_jadot[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_jadot[col] = pd.to_timedelta(df_pt2_jadot[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_jadot[col] = pd.to_timedelta(df_sp1_jadot[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_jadot[col] = pd.to_timedelta(df_sp2_jadot[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_jadot[col] = pd.to_timedelta(df_sp3_jadot[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_jadot["Période"] = "13/03/2022"
    df_sp2_jadot["Période"] = "20/03/2022"
    df_sp3_jadot["Période"] = "27/03/2022"
    df_pt1_jadot["Période"] = "03/04/2022"
    df_pt2_jadot["Période"] = "08/04/2022"

    df_pt1_jadot["Somme"] = (
            df_pt1_jadot['Tranche (6h-9h)(durée)'] + df_pt1_jadot['Tranche (6h-9h)(durée)'] + df_pt1_jadot[
        'Tranche (9h-18h)(durée)'] + df_pt1_jadot['Tranche (18h-24h)(durée)'])

    df_pt2_jadot["Somme"] = (df_pt2_jadot['Tranche (6h-9h)(durée)'] + df_pt2_jadot['Tranche (6h-9h)(durée)'] +
                             df_pt2_jadot['Tranche (9h-18h)(durée)'] + df_pt2_jadot['Tranche (18h-24h)(durée)'])

    df_sp1_jadot["Somme"] = (df_sp1_jadot['Tranche (6h-9h)(durée)'] + df_sp1_jadot['Tranche (6h-9h)(durée)'] +
                             df_sp1_jadot['Tranche (9h-18h)(durée)'] + df_sp1_jadot['Tranche (18h-24h)(durée)'])

    df_sp2_jadot["Somme"] = (df_sp2_jadot['Tranche (6h-9h)(durée)'] + df_sp2_jadot['Tranche (6h-9h)(durée)'] +
                             df_sp2_jadot['Tranche (9h-18h)(durée)'] + df_sp2_jadot['Tranche (18h-24h)(durée)'])

    df_sp3_jadot["Somme"] = (df_sp3_jadot['Tranche (6h-9h)(durée)'] + df_sp3_jadot['Tranche (6h-9h)(durée)'] +
                             df_sp3_jadot['Tranche (9h-18h)(durée)'] + df_sp3_jadot['Tranche (18h-24h)(durée)'])

    df_sp1_jadot['Période'] = pd.to_datetime(df_sp1_jadot['Période'], dayfirst=True)
    df_sp2_jadot['Période'] = pd.to_datetime(df_sp2_jadot['Période'], dayfirst=True)
    df_sp3_jadot['Période'] = pd.to_datetime(df_sp3_jadot['Période'], dayfirst=True)
    df_pt1_jadot['Période'] = pd.to_datetime(df_pt1_jadot['Période'], dayfirst=True)
    df_pt2_jadot['Période'] = pd.to_datetime(df_pt2_jadot['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_jadot = pd.concat([df_sp1_jadot[l], df_sp2_jadot[l], df_sp3_jadot[l], df_pt1_jadot[l], df_pt2_jadot[l]])
    return df_jadot


def get_tdp_lepen():
    df_pt1_lepen = pd.read_csv("lepen/premier_tour_1_lepen.csv", sep=";").fillna(0)
    df_pt2_lepen = pd.read_csv("lepen/premier_tour_2_lepen.csv", sep=";").fillna(0)
    df_sp1_lepen = pd.read_csv("lepen/seconde_periode_1_lepen.csv", sep=";").fillna(0)
    df_sp2_lepen = pd.read_csv("lepen/seconde_periode_2_lepen.csv", sep=";").fillna(0)
    df_sp3_lepen = pd.read_csv("lepen/seconde_periode_3_lepen.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_lepen = df_pt1_lepen[df_pt1_lepen['Candidat'] == type]
    df_pt2_lepen = df_pt2_lepen[df_pt2_lepen['Candidat'] == type]
    df_sp1_lepen = df_sp1_lepen[df_sp1_lepen['Candidat'] == type]
    df_sp2_lepen = df_sp2_lepen[df_sp2_lepen['Candidat'] == type]
    df_sp3_lepen = df_sp3_lepen[df_sp3_lepen['Candidat'] == type]

    df_pt1_lepen.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_lepen.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_lepen.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_lepen.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_lepen.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_lepen.columns[2:]:
        df_pt1_lepen[col] = pd.to_timedelta(df_pt1_lepen[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_lepen[col] = pd.to_timedelta(df_pt2_lepen[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_lepen[col] = pd.to_timedelta(df_sp1_lepen[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_lepen[col] = pd.to_timedelta(df_sp2_lepen[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_lepen[col] = pd.to_timedelta(df_sp3_lepen[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_lepen["Période"] = "13/03/2022"
    df_sp2_lepen["Période"] = "20/03/2022"
    df_sp3_lepen["Période"] = "27/03/2022"
    df_pt1_lepen["Période"] = "03/04/2022"
    df_pt2_lepen["Période"] = "08/04/2022"

    df_pt1_lepen["Somme"] = (
            df_pt1_lepen['Tranche (6h-9h)(durée)'] + df_pt1_lepen['Tranche (6h-9h)(durée)'] + df_pt1_lepen[
        'Tranche (9h-18h)(durée)'] + df_pt1_lepen['Tranche (18h-24h)(durée)'])

    df_pt2_lepen["Somme"] = (df_pt2_lepen['Tranche (6h-9h)(durée)'] + df_pt2_lepen['Tranche (6h-9h)(durée)'] +
                             df_pt2_lepen['Tranche (9h-18h)(durée)'] + df_pt2_lepen['Tranche (18h-24h)(durée)'])

    df_sp1_lepen["Somme"] = (df_sp1_lepen['Tranche (6h-9h)(durée)'] + df_sp1_lepen['Tranche (6h-9h)(durée)'] +
                             df_sp1_lepen['Tranche (9h-18h)(durée)'] + df_sp1_lepen['Tranche (18h-24h)(durée)'])

    df_sp2_lepen["Somme"] = (df_sp2_lepen['Tranche (6h-9h)(durée)'] + df_sp2_lepen['Tranche (6h-9h)(durée)'] +
                             df_sp2_lepen['Tranche (9h-18h)(durée)'] + df_sp2_lepen['Tranche (18h-24h)(durée)'])

    df_sp3_lepen["Somme"] = (df_sp3_lepen['Tranche (6h-9h)(durée)'] + df_sp3_lepen['Tranche (6h-9h)(durée)'] +
                             df_sp3_lepen['Tranche (9h-18h)(durée)'] + df_sp3_lepen['Tranche (18h-24h)(durée)'])

    df_sp1_lepen['Période'] = pd.to_datetime(df_sp1_lepen['Période'], dayfirst=True)
    df_sp2_lepen['Période'] = pd.to_datetime(df_sp2_lepen['Période'], dayfirst=True)
    df_sp3_lepen['Période'] = pd.to_datetime(df_sp3_lepen['Période'], dayfirst=True)
    df_pt1_lepen['Période'] = pd.to_datetime(df_pt1_lepen['Période'], dayfirst=True)
    df_pt2_lepen['Période'] = pd.to_datetime(df_pt2_lepen['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_lepen = pd.concat([df_sp1_lepen[l], df_sp2_lepen[l], df_sp3_lepen[l], df_pt1_lepen[l], df_pt2_lepen[l]])
    return df_lepen


def get_tdp_macron():
    df_pt1_macron = pd.read_csv("macron/premier_tour_1_macron.csv", sep=";").fillna(0)
    df_pt2_macron = pd.read_csv("macron/premier_tour_2_macron.csv", sep=";").fillna(0)
    df_sp1_macron = pd.read_csv("macron/seconde_periode_1_macron.csv", sep=";").fillna(0)
    df_sp2_macron = pd.read_csv("macron/seconde_periode_2_macron.csv", sep=";").fillna(0)
    df_sp3_macron = pd.read_csv("macron/seconde_periode_3_macron.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_macron = df_pt1_macron[df_pt1_macron['Candidat'] == type]
    df_pt2_macron = df_pt2_macron[df_pt2_macron['Candidat'] == type]
    df_sp1_macron = df_sp1_macron[df_sp1_macron['Candidat'] == type]
    df_sp2_macron = df_sp2_macron[df_sp2_macron['Candidat'] == type]
    df_sp3_macron = df_sp3_macron[df_sp3_macron['Candidat'] == type]

    df_pt1_macron.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_macron.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_macron.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_macron.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_macron.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_macron.columns[2:]:
        df_pt1_macron[col] = pd.to_timedelta(df_pt1_macron[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_macron[col] = pd.to_timedelta(df_pt2_macron[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_macron[col] = pd.to_timedelta(df_sp1_macron[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_macron[col] = pd.to_timedelta(df_sp2_macron[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_macron[col] = pd.to_timedelta(df_sp3_macron[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_macron["Période"] = "13/03/2022"
    df_sp2_macron["Période"] = "20/03/2022"
    df_sp3_macron["Période"] = "27/03/2022"
    df_pt1_macron["Période"] = "03/04/2022"
    df_pt2_macron["Période"] = "08/04/2022"

    df_pt1_macron["Somme"] = (
            df_pt1_macron['Tranche (6h-9h)(durée)'] + df_pt1_macron['Tranche (6h-9h)(durée)'] + df_pt1_macron[
        'Tranche (9h-18h)(durée)'] + df_pt1_macron['Tranche (18h-24h)(durée)'])

    df_pt2_macron["Somme"] = (df_pt2_macron['Tranche (6h-9h)(durée)'] + df_pt2_macron['Tranche (6h-9h)(durée)'] +
                              df_pt2_macron['Tranche (9h-18h)(durée)'] + df_pt2_macron['Tranche (18h-24h)(durée)'])

    df_sp1_macron["Somme"] = (df_sp1_macron['Tranche (6h-9h)(durée)'] + df_sp1_macron['Tranche (6h-9h)(durée)'] +
                              df_sp1_macron['Tranche (9h-18h)(durée)'] + df_sp1_macron['Tranche (18h-24h)(durée)'])

    df_sp2_macron["Somme"] = (df_sp2_macron['Tranche (6h-9h)(durée)'] + df_sp2_macron['Tranche (6h-9h)(durée)'] +
                              df_sp2_macron['Tranche (9h-18h)(durée)'] + df_sp2_macron['Tranche (18h-24h)(durée)'])

    df_sp3_macron["Somme"] = (df_sp3_macron['Tranche (6h-9h)(durée)'] + df_sp3_macron['Tranche (6h-9h)(durée)'] +
                              df_sp3_macron['Tranche (9h-18h)(durée)'] + df_sp3_macron['Tranche (18h-24h)(durée)'])

    df_sp1_macron['Période'] = pd.to_datetime(df_sp1_macron['Période'], dayfirst=True)
    df_sp2_macron['Période'] = pd.to_datetime(df_sp2_macron['Période'], dayfirst=True)
    df_sp3_macron['Période'] = pd.to_datetime(df_sp3_macron['Période'], dayfirst=True)
    df_pt1_macron['Période'] = pd.to_datetime(df_pt1_macron['Période'], dayfirst=True)
    df_pt2_macron['Période'] = pd.to_datetime(df_pt2_macron['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_macron = pd.concat([df_sp1_macron[l], df_sp2_macron[l], df_sp3_macron[l], df_pt1_macron[l], df_pt2_macron[l]])
    return df_macron


def get_tdp_melenchon():
    df_pt1_melenchon = pd.read_csv("melenchon/premier_tour_1_melenchon.csv", sep=";").fillna(0)
    df_pt2_melenchon = pd.read_csv("melenchon/premier_tour_2_melenchon.csv", sep=";").fillna(0)
    df_sp1_melenchon = pd.read_csv("melenchon/seconde_periode_1_melenchon.csv", sep=";").fillna(0)
    df_sp2_melenchon = pd.read_csv("melenchon/seconde_periode_2_melenchon.csv", sep=";").fillna(0)
    df_sp3_melenchon = pd.read_csv("melenchon/seconde_periode_3_melenchon.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_melenchon = df_pt1_melenchon[df_pt1_melenchon['Candidat'] == type]
    df_pt2_melenchon = df_pt2_melenchon[df_pt2_melenchon['Candidat'] == type]
    df_sp1_melenchon = df_sp1_melenchon[df_sp1_melenchon['Candidat'] == type]
    df_sp2_melenchon = df_sp2_melenchon[df_sp2_melenchon['Candidat'] == type]
    df_sp3_melenchon = df_sp3_melenchon[df_sp3_melenchon['Candidat'] == type]

    df_pt1_melenchon.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_melenchon.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_melenchon.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_melenchon.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_melenchon.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_melenchon.columns[2:]:
        df_pt1_melenchon[col] = pd.to_timedelta(df_pt1_melenchon[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_melenchon[col] = pd.to_timedelta(df_pt2_melenchon[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_melenchon[col] = pd.to_timedelta(df_sp1_melenchon[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_melenchon[col] = pd.to_timedelta(df_sp2_melenchon[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_melenchon[col] = pd.to_timedelta(df_sp3_melenchon[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_melenchon["Période"] = "13/03/2022"
    df_sp2_melenchon["Période"] = "20/03/2022"
    df_sp3_melenchon["Période"] = "27/03/2022"
    df_pt1_melenchon["Période"] = "03/04/2022"
    df_pt2_melenchon["Période"] = "08/04/2022"

    df_pt1_melenchon["Somme"] = (
            df_pt1_melenchon['Tranche (6h-9h)(durée)'] + df_pt1_melenchon['Tranche (6h-9h)(durée)'] + df_pt1_melenchon[
        'Tranche (9h-18h)(durée)'] + df_pt1_melenchon['Tranche (18h-24h)(durée)'])

    df_pt2_melenchon["Somme"] = (
            df_pt2_melenchon['Tranche (6h-9h)(durée)'] + df_pt2_melenchon['Tranche (6h-9h)(durée)'] +
            df_pt2_melenchon['Tranche (9h-18h)(durée)'] + df_pt2_melenchon['Tranche (18h-24h)(durée)'])

    df_sp1_melenchon["Somme"] = (
            df_sp1_melenchon['Tranche (6h-9h)(durée)'] + df_sp1_melenchon['Tranche (6h-9h)(durée)'] +
            df_sp1_melenchon['Tranche (9h-18h)(durée)'] + df_sp1_melenchon['Tranche (18h-24h)(durée)'])

    df_sp2_melenchon["Somme"] = (
            df_sp2_melenchon['Tranche (6h-9h)(durée)'] + df_sp2_melenchon['Tranche (6h-9h)(durée)'] +
            df_sp2_melenchon['Tranche (9h-18h)(durée)'] + df_sp2_melenchon['Tranche (18h-24h)(durée)'])

    df_sp3_melenchon["Somme"] = (
            df_sp3_melenchon['Tranche (6h-9h)(durée)'] + df_sp3_melenchon['Tranche (6h-9h)(durée)'] +
            df_sp3_melenchon['Tranche (9h-18h)(durée)'] + df_sp3_melenchon['Tranche (18h-24h)(durée)'])

    df_sp1_melenchon['Période'] = pd.to_datetime(df_sp1_melenchon['Période'], dayfirst=True)
    df_sp2_melenchon['Période'] = pd.to_datetime(df_sp2_melenchon['Période'], dayfirst=True)
    df_sp3_melenchon['Période'] = pd.to_datetime(df_sp3_melenchon['Période'], dayfirst=True)
    df_pt1_melenchon['Période'] = pd.to_datetime(df_pt1_melenchon['Période'], dayfirst=True)
    df_pt2_melenchon['Période'] = pd.to_datetime(df_pt2_melenchon['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_melenchon = pd.concat(
        [df_sp1_melenchon[l], df_sp2_melenchon[l], df_sp3_melenchon[l], df_pt1_melenchon[l], df_pt2_melenchon[l]])
    return df_melenchon


def get_tdp_pecresse():
    df_pt1_pecresse = pd.read_csv("pecresse/premier_tour_1_pecresse.csv", sep=";").fillna(0)
    df_pt2_pecresse = pd.read_csv("pecresse/premier_tour_2_pecresse.csv", sep=";").fillna(0)
    df_sp1_pecresse = pd.read_csv("pecresse/seconde_periode_1_pecresse.csv", sep=";").fillna(0)
    df_sp2_pecresse = pd.read_csv("pecresse/seconde_periode_2_pecresse.csv", sep=";").fillna(0)
    df_sp3_pecresse = pd.read_csv("pecresse/seconde_periode_3_pecresse.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_pecresse = df_pt1_pecresse[df_pt1_pecresse['Candidat'] == type]
    df_pt2_pecresse = df_pt2_pecresse[df_pt2_pecresse['Candidat'] == type]
    df_sp1_pecresse = df_sp1_pecresse[df_sp1_pecresse['Candidat'] == type]
    df_sp2_pecresse = df_sp2_pecresse[df_sp2_pecresse['Candidat'] == type]
    df_sp3_pecresse = df_sp3_pecresse[df_sp3_pecresse['Candidat'] == type]

    df_pt1_pecresse.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_pecresse.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_pecresse.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_pecresse.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_pecresse.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_pecresse.columns[2:]:
        df_pt1_pecresse[col] = pd.to_timedelta(df_pt1_pecresse[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_pecresse[col] = pd.to_timedelta(df_pt2_pecresse[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_pecresse[col] = pd.to_timedelta(df_sp1_pecresse[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_pecresse[col] = pd.to_timedelta(df_sp2_pecresse[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_pecresse[col] = pd.to_timedelta(df_sp3_pecresse[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_pecresse["Période"] = "13/03/2022"
    df_sp2_pecresse["Période"] = "20/03/2022"
    df_sp3_pecresse["Période"] = "27/03/2022"
    df_pt1_pecresse["Période"] = "03/04/2022"
    df_pt2_pecresse["Période"] = "08/04/2022"

    df_pt1_pecresse["Somme"] = (
            df_pt1_pecresse['Tranche (6h-9h)(durée)'] + df_pt1_pecresse['Tranche (6h-9h)(durée)'] + df_pt1_pecresse[
        'Tranche (9h-18h)(durée)'] + df_pt1_pecresse['Tranche (18h-24h)(durée)'])

    df_pt2_pecresse["Somme"] = (df_pt2_pecresse['Tranche (6h-9h)(durée)'] + df_pt2_pecresse['Tranche (6h-9h)(durée)'] +
                                df_pt2_pecresse['Tranche (9h-18h)(durée)'] + df_pt2_pecresse[
                                    'Tranche (18h-24h)(durée)'])

    df_sp1_pecresse["Somme"] = (df_sp1_pecresse['Tranche (6h-9h)(durée)'] + df_sp1_pecresse['Tranche (6h-9h)(durée)'] +
                                df_sp1_pecresse['Tranche (9h-18h)(durée)'] + df_sp1_pecresse[
                                    'Tranche (18h-24h)(durée)'])

    df_sp2_pecresse["Somme"] = (df_sp2_pecresse['Tranche (6h-9h)(durée)'] + df_sp2_pecresse['Tranche (6h-9h)(durée)'] +
                                df_sp2_pecresse['Tranche (9h-18h)(durée)'] + df_sp2_pecresse[
                                    'Tranche (18h-24h)(durée)'])

    df_sp3_pecresse["Somme"] = (df_sp3_pecresse['Tranche (6h-9h)(durée)'] + df_sp3_pecresse['Tranche (6h-9h)(durée)'] +
                                df_sp3_pecresse['Tranche (9h-18h)(durée)'] + df_sp3_pecresse[
                                    'Tranche (18h-24h)(durée)'])

    df_sp1_pecresse['Période'] = pd.to_datetime(df_sp1_pecresse['Période'], dayfirst=True)
    df_sp2_pecresse['Période'] = pd.to_datetime(df_sp2_pecresse['Période'], dayfirst=True)
    df_sp3_pecresse['Période'] = pd.to_datetime(df_sp3_pecresse['Période'], dayfirst=True)
    df_pt1_pecresse['Période'] = pd.to_datetime(df_pt1_pecresse['Période'], dayfirst=True)
    df_pt2_pecresse['Période'] = pd.to_datetime(df_pt2_pecresse['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_pecresse = pd.concat(
        [df_sp1_pecresse[l], df_sp2_pecresse[l], df_sp3_pecresse[l], df_pt1_pecresse[l], df_pt2_pecresse[l]])
    return df_pecresse


def get_tdp_poutou():
    df_pt1_poutou = pd.read_csv("poutou/premier_tour_1_poutou.csv", sep=";").fillna(0)
    df_pt2_poutou = pd.read_csv("poutou/premier_tour_2_poutou.csv", sep=";").fillna(0)
    df_sp1_poutou = pd.read_csv("poutou/seconde_periode_1_poutou.csv", sep=";").fillna(0)
    df_sp2_poutou = pd.read_csv("poutou/seconde_periode_2_poutou.csv", sep=";").fillna(0)
    df_sp3_poutou = pd.read_csv("poutou/seconde_periode_3_poutou.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_poutou = df_pt1_poutou[df_pt1_poutou['Candidat'] == type]
    df_pt2_poutou = df_pt2_poutou[df_pt2_poutou['Candidat'] == type]
    df_sp1_poutou = df_sp1_poutou[df_sp1_poutou['Candidat'] == type]
    df_sp2_poutou = df_sp2_poutou[df_sp2_poutou['Candidat'] == type]
    df_sp3_poutou = df_sp3_poutou[df_sp3_poutou['Candidat'] == type]

    df_pt1_poutou.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_poutou.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_poutou.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_poutou.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_poutou.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_poutou.columns[2:]:
        df_pt1_poutou[col] = pd.to_timedelta(df_pt1_poutou[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_poutou[col] = pd.to_timedelta(df_pt2_poutou[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_poutou[col] = pd.to_timedelta(df_sp1_poutou[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_poutou[col] = pd.to_timedelta(df_sp2_poutou[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_poutou[col] = pd.to_timedelta(df_sp3_poutou[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_poutou["Période"] = "13/03/2022"
    df_sp2_poutou["Période"] = "20/03/2022"
    df_sp3_poutou["Période"] = "27/03/2022"
    df_pt1_poutou["Période"] = "03/04/2022"
    df_pt2_poutou["Période"] = "08/04/2022"

    df_pt1_poutou["Somme"] = (
            df_pt1_poutou['Tranche (6h-9h)(durée)'] + df_pt1_poutou['Tranche (6h-9h)(durée)'] + df_pt1_poutou[
        'Tranche (9h-18h)(durée)'] + df_pt1_poutou['Tranche (18h-24h)(durée)'])

    df_pt2_poutou["Somme"] = (df_pt2_poutou['Tranche (6h-9h)(durée)'] + df_pt2_poutou['Tranche (6h-9h)(durée)'] +
                              df_pt2_poutou['Tranche (9h-18h)(durée)'] + df_pt2_poutou['Tranche (18h-24h)(durée)'])

    df_sp1_poutou["Somme"] = (df_sp1_poutou['Tranche (6h-9h)(durée)'] + df_sp1_poutou['Tranche (6h-9h)(durée)'] +
                              df_sp1_poutou['Tranche (9h-18h)(durée)'] + df_sp1_poutou['Tranche (18h-24h)(durée)'])

    df_sp2_poutou["Somme"] = (df_sp2_poutou['Tranche (6h-9h)(durée)'] + df_sp2_poutou['Tranche (6h-9h)(durée)'] +
                              df_sp2_poutou['Tranche (9h-18h)(durée)'] + df_sp2_poutou['Tranche (18h-24h)(durée)'])

    df_sp3_poutou["Somme"] = (df_sp3_poutou['Tranche (6h-9h)(durée)'] + df_sp3_poutou['Tranche (6h-9h)(durée)'] +
                              df_sp3_poutou['Tranche (9h-18h)(durée)'] + df_sp3_poutou['Tranche (18h-24h)(durée)'])

    df_sp1_poutou['Période'] = pd.to_datetime(df_sp1_poutou['Période'], dayfirst=True)
    df_sp2_poutou['Période'] = pd.to_datetime(df_sp2_poutou['Période'], dayfirst=True)
    df_sp3_poutou['Période'] = pd.to_datetime(df_sp3_poutou['Période'], dayfirst=True)
    df_pt1_poutou['Période'] = pd.to_datetime(df_pt1_poutou['Période'], dayfirst=True)
    df_pt2_poutou['Période'] = pd.to_datetime(df_pt2_poutou['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_poutou = pd.concat([df_sp1_poutou[l], df_sp2_poutou[l], df_sp3_poutou[l], df_pt1_poutou[l], df_pt2_poutou[l]])
    return df_poutou


def get_tdp_roussel():
    df_pt1_roussel = pd.read_csv("roussel/premier_tour_1_roussel.csv", sep=";").fillna(0)
    df_pt2_roussel = pd.read_csv("roussel/premier_tour_2_roussel.csv", sep=";").fillna(0)
    df_sp1_roussel = pd.read_csv("roussel/seconde_periode_1_roussel.csv", sep=";").fillna(0)
    df_sp2_roussel = pd.read_csv("roussel/seconde_periode_2_roussel.csv", sep=";").fillna(0)
    df_sp3_roussel = pd.read_csv("roussel/seconde_periode_3_roussel.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_roussel = df_pt1_roussel[df_pt1_roussel['Candidat'] == type]
    df_pt2_roussel = df_pt2_roussel[df_pt2_roussel['Candidat'] == type]
    df_sp1_roussel = df_sp1_roussel[df_sp1_roussel['Candidat'] == type]
    df_sp2_roussel = df_sp2_roussel[df_sp2_roussel['Candidat'] == type]
    df_sp3_roussel = df_sp3_roussel[df_sp3_roussel['Candidat'] == type]

    df_pt1_roussel.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_roussel.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_roussel.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_roussel.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_roussel.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_roussel.columns[2:]:
        df_pt1_roussel[col] = pd.to_timedelta(df_pt1_roussel[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_roussel[col] = pd.to_timedelta(df_pt2_roussel[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_roussel[col] = pd.to_timedelta(df_sp1_roussel[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_roussel[col] = pd.to_timedelta(df_sp2_roussel[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_roussel[col] = pd.to_timedelta(df_sp3_roussel[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_roussel["Période"] = "13/03/2022"
    df_sp2_roussel["Période"] = "20/03/2022"
    df_sp3_roussel["Période"] = "27/03/2022"
    df_pt1_roussel["Période"] = "03/04/2022"
    df_pt2_roussel["Période"] = "08/04/2022"

    df_pt1_roussel["Somme"] = (
            df_pt1_roussel['Tranche (6h-9h)(durée)'] + df_pt1_roussel['Tranche (6h-9h)(durée)'] + df_pt1_roussel[
        'Tranche (9h-18h)(durée)'] + df_pt1_roussel['Tranche (18h-24h)(durée)'])

    df_pt2_roussel["Somme"] = (df_pt2_roussel['Tranche (6h-9h)(durée)'] + df_pt2_roussel['Tranche (6h-9h)(durée)'] +
                               df_pt2_roussel['Tranche (9h-18h)(durée)'] + df_pt2_roussel['Tranche (18h-24h)(durée)'])

    df_sp1_roussel["Somme"] = (df_sp1_roussel['Tranche (6h-9h)(durée)'] + df_sp1_roussel['Tranche (6h-9h)(durée)'] +
                               df_sp1_roussel['Tranche (9h-18h)(durée)'] + df_sp1_roussel['Tranche (18h-24h)(durée)'])

    df_sp2_roussel["Somme"] = (df_sp2_roussel['Tranche (6h-9h)(durée)'] + df_sp2_roussel['Tranche (6h-9h)(durée)'] +
                               df_sp2_roussel['Tranche (9h-18h)(durée)'] + df_sp2_roussel['Tranche (18h-24h)(durée)'])

    df_sp3_roussel["Somme"] = (df_sp3_roussel['Tranche (6h-9h)(durée)'] + df_sp3_roussel['Tranche (6h-9h)(durée)'] +
                               df_sp3_roussel['Tranche (9h-18h)(durée)'] + df_sp3_roussel['Tranche (18h-24h)(durée)'])

    df_sp1_roussel['Période'] = pd.to_datetime(df_sp1_roussel['Période'], dayfirst=True)
    df_sp2_roussel['Période'] = pd.to_datetime(df_sp2_roussel['Période'], dayfirst=True)
    df_sp3_roussel['Période'] = pd.to_datetime(df_sp3_roussel['Période'], dayfirst=True)
    df_pt1_roussel['Période'] = pd.to_datetime(df_pt1_roussel['Période'], dayfirst=True)
    df_pt2_roussel['Période'] = pd.to_datetime(df_pt2_roussel['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_roussel = pd.concat(
        [df_sp1_roussel[l], df_sp2_roussel[l], df_sp3_roussel[l], df_pt1_roussel[l], df_pt2_roussel[l]])
    return df_roussel


def get_tdp_zemmour():
    df_pt1_zemmour = pd.read_csv("zemmour/premier_tour_1_zemmour.csv", sep=";").fillna(0)
    df_pt2_zemmour = pd.read_csv("zemmour/premier_tour_2_zemmour.csv", sep=";").fillna(0)
    df_sp1_zemmour = pd.read_csv("zemmour/seconde_periode_1_zemmour.csv", sep=";").fillna(0)
    df_sp2_zemmour = pd.read_csv("zemmour/seconde_periode_2_zemmour.csv", sep=";").fillna(0)
    df_sp3_zemmour = pd.read_csv("zemmour/seconde_periode_3_zemmour.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_zemmour = df_pt1_zemmour[df_pt1_zemmour['Candidat'] == type]
    df_pt2_zemmour = df_pt2_zemmour[df_pt2_zemmour['Candidat'] == type]
    df_sp1_zemmour = df_sp1_zemmour[df_sp1_zemmour['Candidat'] == type]
    df_sp2_zemmour = df_sp2_zemmour[df_sp2_zemmour['Candidat'] == type]
    df_sp3_zemmour = df_sp3_zemmour[df_sp3_zemmour['Candidat'] == type]

    df_pt1_zemmour.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_zemmour.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_zemmour.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_zemmour.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_zemmour.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_zemmour.columns[2:]:
        df_pt1_zemmour[col] = pd.to_timedelta(df_pt1_zemmour[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_zemmour[col] = pd.to_timedelta(df_pt2_zemmour[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_zemmour[col] = pd.to_timedelta(df_sp1_zemmour[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_zemmour[col] = pd.to_timedelta(df_sp2_zemmour[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_zemmour[col] = pd.to_timedelta(df_sp3_zemmour[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_zemmour["Période"] = "13/03/2022"
    df_sp2_zemmour["Période"] = "20/03/2022"
    df_sp3_zemmour["Période"] = "27/03/2022"
    df_pt1_zemmour["Période"] = "03/04/2022"
    df_pt2_zemmour["Période"] = "08/04/2022"

    df_pt1_zemmour["Somme"] = (
            df_pt1_zemmour['Tranche (6h-9h)(durée)'] + df_pt1_zemmour['Tranche (6h-9h)(durée)'] + df_pt1_zemmour[
        'Tranche (9h-18h)(durée)'] + df_pt1_zemmour['Tranche (18h-24h)(durée)'])

    df_pt2_zemmour["Somme"] = (df_pt2_zemmour['Tranche (6h-9h)(durée)'] + df_pt2_zemmour['Tranche (6h-9h)(durée)'] +
                               df_pt2_zemmour['Tranche (9h-18h)(durée)'] + df_pt2_zemmour['Tranche (18h-24h)(durée)'])

    df_sp1_zemmour["Somme"] = (df_sp1_zemmour['Tranche (6h-9h)(durée)'] + df_sp1_zemmour['Tranche (6h-9h)(durée)'] +
                               df_sp1_zemmour['Tranche (9h-18h)(durée)'] + df_sp1_zemmour['Tranche (18h-24h)(durée)'])

    df_sp2_zemmour["Somme"] = (df_sp2_zemmour['Tranche (6h-9h)(durée)'] + df_sp2_zemmour['Tranche (6h-9h)(durée)'] +
                               df_sp2_zemmour['Tranche (9h-18h)(durée)'] + df_sp2_zemmour['Tranche (18h-24h)(durée)'])

    df_sp3_zemmour["Somme"] = (df_sp3_zemmour['Tranche (6h-9h)(durée)'] + df_sp3_zemmour['Tranche (6h-9h)(durée)'] +
                               df_sp3_zemmour['Tranche (9h-18h)(durée)'] + df_sp3_zemmour['Tranche (18h-24h)(durée)'])

    df_sp1_zemmour['Période'] = pd.to_datetime(df_sp1_zemmour['Période'], dayfirst=True)
    df_sp2_zemmour['Période'] = pd.to_datetime(df_sp2_zemmour['Période'], dayfirst=True)
    df_sp3_zemmour['Période'] = pd.to_datetime(df_sp3_zemmour['Période'], dayfirst=True)
    df_pt1_zemmour['Période'] = pd.to_datetime(df_pt1_zemmour['Période'], dayfirst=True)
    df_pt2_zemmour['Période'] = pd.to_datetime(df_pt2_zemmour['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_zemmour = pd.concat(
        [df_sp1_zemmour[l], df_sp2_zemmour[l], df_sp3_zemmour[l], df_pt1_zemmour[l], df_pt2_zemmour[l]])
    return df_zemmour


def get_tdp_lassalle():
    df_pt1_lassalle = pd.read_csv("lassalle/premier_tour_1_lassalle.csv", sep=";").fillna(0)
    df_pt2_lassalle = pd.read_csv("lassalle/premier_tour_2_lassalle.csv", sep=";").fillna(0)
    df_sp1_lassalle = pd.read_csv("lassalle/seconde_periode_1_lassalle.csv", sep=";").fillna(0)
    df_sp2_lassalle = pd.read_csv("lassalle/seconde_periode_2_lassalle.csv", sep=";").fillna(0)
    df_sp3_lassalle = pd.read_csv("lassalle/seconde_periode_3_lassalle.csv", sep=";").fillna(0)

    type = "Total temps de parole"
    df_pt1_lassalle = df_pt1_lassalle[df_pt1_lassalle['Candidat'] == type]
    df_pt2_lassalle = df_pt2_lassalle[df_pt2_lassalle['Candidat'] == type]
    df_sp1_lassalle = df_sp1_lassalle[df_sp1_lassalle['Candidat'] == type]
    df_sp2_lassalle = df_sp2_lassalle[df_sp2_lassalle['Candidat'] == type]
    df_sp3_lassalle = df_sp3_lassalle[df_sp3_lassalle['Candidat'] == type]

    df_pt1_lassalle.drop(['Détail des temps'], axis=1, inplace=True)
    df_pt2_lassalle.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp1_lassalle.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp2_lassalle.drop(['Détail des temps'], axis=1, inplace=True)
    df_sp3_lassalle.drop(['Détail des temps'], axis=1, inplace=True)

    for col in df_pt1_lassalle.columns[2:]:
        df_pt1_lassalle[col] = pd.to_timedelta(df_pt1_lassalle[col]) / (60 * pd.Timedelta('1s'))
        df_pt2_lassalle[col] = pd.to_timedelta(df_pt2_lassalle[col]) / (60 * pd.Timedelta('1s'))
        df_sp1_lassalle[col] = pd.to_timedelta(df_sp1_lassalle[col]) / (60 * pd.Timedelta('1s'))
        df_sp2_lassalle[col] = pd.to_timedelta(df_sp2_lassalle[col]) / (60 * pd.Timedelta('1s'))
        df_sp3_lassalle[col] = pd.to_timedelta(df_sp3_lassalle[col]) / (60 * pd.Timedelta('1s'))

    df_sp1_lassalle["Période"] = "13/03/2022"
    df_sp2_lassalle["Période"] = "20/03/2022"
    df_sp3_lassalle["Période"] = "27/03/2022"
    df_pt1_lassalle["Période"] = "03/04/2022"
    df_pt2_lassalle["Période"] = "08/04/2022"

    df_pt1_lassalle["Somme"] = (
            df_pt1_lassalle['Tranche (6h-9h)(durée)'] + df_pt1_lassalle['Tranche (6h-9h)(durée)'] + df_pt1_lassalle[
        'Tranche (9h-18h)(durée)'] + df_pt1_lassalle['Tranche (18h-24h)(durée)'])

    df_pt2_lassalle["Somme"] = (df_pt2_lassalle['Tranche (6h-9h)(durée)'] + df_pt2_lassalle['Tranche (6h-9h)(durée)'] +
                                df_pt2_lassalle['Tranche (9h-18h)(durée)'] + df_pt2_lassalle[
                                    'Tranche (18h-24h)(durée)'])

    df_sp1_lassalle["Somme"] = (df_sp1_lassalle['Tranche (6h-9h)(durée)'] + df_sp1_lassalle['Tranche (6h-9h)(durée)'] +
                                df_sp1_lassalle['Tranche (9h-18h)(durée)'] + df_sp1_lassalle[
                                    'Tranche (18h-24h)(durée)'])

    df_sp2_lassalle["Somme"] = (df_sp2_lassalle['Tranche (6h-9h)(durée)'] + df_sp2_lassalle['Tranche (6h-9h)(durée)'] +
                                df_sp2_lassalle['Tranche (9h-18h)(durée)'] + df_sp2_lassalle[
                                    'Tranche (18h-24h)(durée)'])

    df_sp3_lassalle["Somme"] = (df_sp3_lassalle['Tranche (6h-9h)(durée)'] + df_sp3_lassalle['Tranche (6h-9h)(durée)'] +
                                df_sp3_lassalle['Tranche (9h-18h)(durée)'] + df_sp3_lassalle[
                                    'Tranche (18h-24h)(durée)'])

    df_sp1_lassalle['Période'] = pd.to_datetime(df_sp1_lassalle['Période'], dayfirst=True)
    df_sp2_lassalle['Période'] = pd.to_datetime(df_sp2_lassalle['Période'], dayfirst=True)
    df_sp3_lassalle['Période'] = pd.to_datetime(df_sp3_lassalle['Période'], dayfirst=True)
    df_pt1_lassalle['Période'] = pd.to_datetime(df_pt1_lassalle['Période'], dayfirst=True)
    df_pt2_lassalle['Période'] = pd.to_datetime(df_pt2_lassalle['Période'], dayfirst=True)

    l = ['Chaîne', 'Période', 'Somme']

    df_lassalle = pd.concat(
        [df_sp1_lassalle[l], df_sp2_lassalle[l], df_sp3_lassalle[l], df_pt1_lassalle[l], df_pt2_lassalle[l]])
    return df_lassalle


def get_temps_de_parole():
    df_macron = get_tdp_macron()
    df_lepen = get_tdp_lepen()
    df_poutou = get_tdp_poutou()
    df_pecresse = get_tdp_pecresse()
    df_hidalgo = get_tdp_hidalgo()
    df_arthaud = get_tdp_arthaud()
    df_dupont = get_tdp_dupont()
    df_jadot = get_tdp_jadot()
    df_melenchon = get_tdp_melenchon()
    df_roussel = get_tdp_roussel()
    df_zemmour = get_tdp_zemmour()
    df_lassalle = get_tdp_lassalle()

    df_arthaud['Candidat'] = "Arthaud"
    df_dupont['Candidat'] = "Dupont"
    df_hidalgo['Candidat'] = "Hidalgo"
    df_jadot['Candidat'] = "Jadot"
    df_lassalle['Candidat'] = "Lassalle"
    df_lepen['Candidat'] = "Lepen"
    df_macron['Candidat'] = "Macron"
    df_melenchon['Candidat'] = "Mélenchon"
    df_pecresse['Candidat'] = "Pecresse"
    df_poutou['Candidat'] = "Poutou"
    df_roussel['Candidat'] = "Roussel"
    df_zemmour['Candidat'] = "Zemmour"

    df_result = pd.concat([df_arthaud, df_dupont, df_hidalgo, df_jadot,
                           df_lassalle, df_lepen, df_macron, df_melenchon,
                           df_pecresse, df_poutou, df_roussel, df_zemmour], axis=0)
    df_result.to_csv('temps_de_parole_presidentielles_2022.csv')


if __name__ == '__main__':
    get_sondage_tour_1()
    get_sondage_tour_2()
    get_temps_de_parole()
