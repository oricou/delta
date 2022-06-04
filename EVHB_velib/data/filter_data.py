# Removes older columns (not needed anymore)

from os import sep
import numpy as np
import plotly.graph_objects as go
import json
import glob
import os
import pandas as pd


for path in glob.glob('data/velib/clean_[0-9]*'):
    print(path)

    df = pd.read_csv(path, sep=";")
    df.drop(["ratio_pop", "ratio_pop_log", "ratio_avail",
            "ratio_avail_log"], axis=1, inplace=True)

    df.to_csv(path, sep=";", index_label=False, index=False)
