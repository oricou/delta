import pandas as pd

# ######################################
# Static data
# ######################################

about_md = "L'objectif du projet est de visualiser un jeu de données à la facon des cas du projet [Δelta](https://delta.lrde.epita.fr/). Le projet se fait en binôme et a été réalisé par Adrien Barens et William Guillet"

documentation_lexique = """
##### Sources
Ce projet a été construit à partir de datasets récupérés sur [www.data.gouv.fr](www.data.gouv.fr)

Cinq datasets ont été récupérés. Un dataset concerne APB qui était la platforme de choix des voeux pour le supérieur entre 2009 à 2017. Cependant, ce dataset contient uniquement des données de 2016 jusqu'à 2017. Aucun datasets retraçant des données avant 2016 n'a été retrouvé. Puis, quatre autres datasets concernant cette fois Parcoursup ont été récupérés. Chacun couvre une année de 2018 jusqu'à 2021.
- [APB Voeux de poursuite d'étude et admissions](https://www.data.gouv.fr/fr/datasets/apb-voeux-de-poursuite-detude-et-admissions/#description)
- [Parcoursup 2018 - vœux de poursuite d'études et de réorientation dans l'enseignement supérieur et réponses des établissements](https://www.data.gouv.fr/fr/datasets/parcoursup-2018-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements-1/)
- [Parcoursup 2019 - vœux de poursuite d'études et de réorientation dans l'enseignement supérieur et réponses des établissements](https://www.data.gouv.fr/fr/datasets/parcoursup-2019-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements-2/)
- [Parcoursup 2020 - vœux de poursuite d'études et de réorientation dans l'enseignement supérieur et réponses des établissements](https://www.data.gouv.fr/fr/datasets/parcoursup-2020-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements/)
- [Parcoursup 2021 - vœux de poursuite d'études et de réorientation dans l'enseignement supérieur et réponses des établissements](https://www.data.gouv.fr/fr/datasets/parcoursup-2021-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements/)


##### Données récupérées
Plusieurs colonnes ont été extraitent de ces datasets. Il y avait une différence dans les noms de colonnes entre le dataset d'APB et le dataset de Parcoursup. Par exemple sur APB `acc_tot_f` devient `Effectif total des candidats ayant accepté la proposition de l’établissement (admis)` sur Parcoursup. Cependant, la correspondance entre les colonnes a pu facilement être établit grâce à la description des datasets de Parcoursup qui donne directement les équivalences par rapport aux anciens noms :

![Parcoursup description](./assets/parcoursup_description.png)

Au final, une dixaine de colonnes ont été gardées :
 - Session : Année de la formulation des voeux
 - Code UAI de l'établissement : Code permettant d'identifier les établissements
 - Établissement : Nom de l'établissement
 - Département de l’établissement : Nom du département
 - Filière de formation très agrégée
 - Filière de formation
 - Filière de formation très détaillée
 - Capacité de l’établissement par formation
 - Effectif total des candidats ayant accepté la proposition de l’établissement (admis)
 - Dont effectif des candidates admises


##### Explications
###### 1) de DUT à BUT
On peut se questionner sur certaines données que l'on observe. Notamment, on peut remarquer sur l'histogramme des DUT / BUT que les DUT Service et Production ont des données entre 2016 et 2020 mais qu'en 2021 le nombre d'étudiant est nul. A l'inverse les BUT Service et Production n'ont aucun étudiants entre 2016 et 2020 alors qu'2021 cette valeur n'est plus nulle. 

![Histogramme des DUT et BUT Service et Production](./assets/histogramme_dut_but.png)

Cela s'explique par les changements récents sur ce cursus. En effet, les DUT (diplômes en 2 ans) ont été remplacés par les BUT qui fusionnent DUT et licence professionnelle (1 à 3 ans souvent prise après un DUT pour se spécialiser)

![Extrait d'article sur le passage de DUT à BUT](./assets/but_info.png)

source : [L'etudiant](https://www.letudiant.fr/etudes/btsdut/des-dut-aux-but-le-point-sur-le-nouveau-bachelor-universitaire-de-technologie.html)


###### 2) de PACES à PASS
De la même façon, que pour les DUT, il y a eu un renommage pour PACES qui s'appelle desormais PASS et qui apporte avec lui son lot de changement également.

source: [La réforme des études de santé](https://pass-sante.com/pass-parcours-acces-sante-specifique-la-nouvelle-paces/)
"""

# ######################################
# Load data
# ######################################

dataset_paths = [
    "./ab_wg_apb_parcoursup/data/apb_2016_2017.csv",
    "./ab_wg_apb_parcoursup/data/parcoursup_2018.csv",
    "./ab_wg_apb_parcoursup/data/parcoursup_2019.csv",
    "./ab_wg_apb_parcoursup/data/parcoursup_2020.csv",
    "./ab_wg_apb_parcoursup/data/parcoursup_2021.csv",
]

FORMATED_COLOMN_NAMES = [
    "session",
    "uai",
    "etablissement",
    "departement",
    "formation",
    "formation details",
    "description",
    "nb places",
    "nb etudiants",
    "nb filles",
]

APB_COLOMN_NAMES = [
    "session",
    "cod_uai",
    "g_ea_lib_vx",
    "lib_dep",
    "fili",
    "form_lib_voe_acc",
    "fil_lib_voe_acc",
    "capa_fin",
    "acc_tot",
    "acc_tot_f",
]

PARCOURSUP_COLOMN_NAMES = [
    "Session",
    "Code UAI de l'établissement",
    "Établissement",
    "Département de l’établissement",
    "Filière de formation très agrégée",
    "Filière de formation",
    "Filière de formation très détaillée",
    "Capacité de l’établissement par formation",
    "Effectif total des candidats ayant accepté la proposition de l’établissement (admis)",
    "Dont effectif des candidates admises",
]


def normalize_formation(row):
    if row == "8_Ingénieur":
        return "Ecole d'Ingénieur"
    elif row == "Autre":
        return "Autre formation"

    row = row.replace("_", "")
    return "".join(filter(lambda x: not x.isdigit(), row))


def get_data():
    """
    Colonnes retenues:
        Session
        Établissement
        Département de l’établissement
        Code départemental de l’établissement
        Effectif total des candidats ayant accepté la proposition de l’établissement (admis)
        Filière de formation très agrégée
        Filière de formation
    """
    datasets = []
    for path in dataset_paths:
        df = pd.read_csv(path, delimiter=";")

        if "2016" in path:
            df = df[APB_COLOMN_NAMES]
            df.set_axis(FORMATED_COLOMN_NAMES, axis=1, inplace=True)
        else:
            df = df[PARCOURSUP_COLOMN_NAMES]
            df.set_axis(FORMATED_COLOMN_NAMES, axis=1, inplace=True)
        datasets.append(df)

    df = pd.concat(datasets)

    df["nb etudiants"] = pd.to_numeric(df["nb etudiants"], errors="coerce")
    df["nb filles"] = pd.to_numeric(df["nb filles"], errors="coerce")
    df["nb places"] = pd.to_numeric(df["nb places"], errors="coerce")
    df["formation"] = df["formation"].apply(normalize_formation)

    return df
