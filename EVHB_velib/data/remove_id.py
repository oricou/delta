# From a corrupted csv, removes wrong columns

from os import sep
import plotly.graph_objects as go
import json
import glob
import os
import pandas as pd


for path in glob.glob('data/velib/clean_[0-9]*'):
    print(path)
    df = pd.read_csv(path, sep=";")
    try:
        df.drop("Unnamed: 0", axis=1, inplace=True)
    except:
        continue
    df.to_csv(path, sep=";", index_label=False, index=False)
