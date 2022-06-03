#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


PATH_RESOURCES = Path("TBGT_population_vs_train_speed/data")
TRAIN_PATH = PATH_RESOURCES / "meilleurs-temps-des-parcours-des-trains.csv"
POPUL_PATH = PATH_RESOURCES / "base-pop-historiques-1876-2019.xlsx"
CITIE_PATH = PATH_RESOURCES / "cities.json"

Coords = Tuple[float, float]


def _clean_train(train_df: pd.DataFrame) -> None:
    train_df.loc[train_df["Relations"] == "PARIS - BOULOGNE", "Relations"] = "PARIS - BOULOGNE-SUR-MER"
    train_df.loc[train_df["Relations"] == "PARIS - CHERBOURG", "Relations"] = "PARIS - CHERBOURG-EN-COTENTIN"
    train_df.loc[train_df["Relations"] == "PARIS - CLERMONT FERRAND", "Relations"] = "PARIS - CLERMONT-FERRAND"
    train_df.loc[train_df["Relations"] == "PARIS - ST ETIENNE", "Relations"] = "PARIS - SAINT-ETIENNE"

def get_train_data() -> pd.core.groupby.DataFrameGroupBy:
    train_df = pd.read_csv(TRAIN_PATH, sep=";")
    train_df.sort_values("Année", inplace=True)
    train_df.sort_values("Relations", inplace=True, kind='stable')
    _clean_train(train_df)

    return train_df

def get_cities() -> dict[str, Coords]:
    with open(CITIE_PATH, "r") as f:
        cities = json.load(f)

    return cities

def _clean_pop_index(pop_df: pd.DataFrame) -> pd.DataFrame:
    # Remove useless columns/ rows
    pop_df = pop_df.drop(index=[0,1,2]).drop(columns=pop_df.columns[0:3])
    pop_df.columns = pop_df.iloc[0]
    pop_df.drop(index=[3,4], inplace=True)

    # Rename cities column
    pop_df = pop_df.set_index("Libellé géographique")
    pop_df.columns = [[int(s) for s in name.split() if s.isdigit()][0] for name in pop_df.columns]
    pop_df.index = pop_df.index.str.upper()
    pop_df.index = pop_df.index.str.replace(u"É","E")

    # Compute Paris as a single city
    paris = pop_df.loc["PARIS 1ER ARRONDISSEMENT":"PARIS 20E ARRONDISSEMENT"].sum()
    paris.name = "PARIS"
    pop_df = pop_df.append(paris.transpose())

    # Sort on years
    pop_df = pop_df.transpose()
    pop_df = pop_df.sort_index()

    # Filter out unused cities
    cities = get_cities().keys()
    pop_df = pop_df[cities]

    # Remove duplicate cities
    pop_df = pop_df.loc[:, ~pop_df.columns.duplicated()]

    # Interpolate lacking data
    pop_df = pop_df.reindex(list(range(pop_df.index.min(),pop_df.index.max()+1)))
    pop_df = pop_df.infer_objects()
    pop_df = pop_df.interpolate()
    pop_df = pop_df.pct_change().mul(100)

    return pop_df

def get_population_data() -> pd.DataFrame:
    pop_df = pd.read_excel("TBGT_population_vs_train_speed/data/base-pop-historiques-1876-2019.xlsx")
    return _clean_pop_index(pop_df)
