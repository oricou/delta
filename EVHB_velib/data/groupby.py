# Grouping all rows by arrond

from os import sep
import numpy as np
import plotly.graph_objects as go
import json
import glob
import os
import pandas as pd


for path in glob.glob('data/velib/clean_[0-9]*'):
    print(path)
    grouped = path.replace("data/velib/clean_", "data/velib/grouped_")

    df = pd.read_csv(path, sep=";")

    out = df[["arrond", "capacity", "avail. bike"]]

    out = out.groupby(by='arrond').sum().reset_index()

    out.to_csv(grouped, sep=";", index_label=False, index=False)
