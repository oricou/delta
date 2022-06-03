# Computes needed data to plot the avail. line

from operator import le
from os import sep
from time import strftime
import numpy as np
import plotly.graph_objects as go
import json
import glob
import os
import pandas as pd


out = pd.DataFrame({"hour": [], "avail. bike": [], "capacity": []})

for path in glob.glob('data/velib/grouped_2022_03_11_[0-9]*'):
    print(path)
    out_path = path.replace('data/velib/grouped_', 'data/velib/col_sum_')
    date = path.replace('data/velib/grouped_',
                        '').replace('_velib.csv', '')[8:]

    df = pd.read_csv(path, sep=";")
    capacity, avail = df[['capacity', 'avail. bike']].sum()

    out = pd.concat(
        [out, pd.DataFrame({"hour": [date], "avail. bike": [
                           avail], "capacity": [capacity]})],
        ignore_index=True)


out.sort_values(by='hour', inplace=True)
out.drop(out[out["capacity"] != 44953].index, inplace=True)
print(out)

out.to_csv("data/velib/col_sum_velib.csv",
           sep=";", index_label=False, index=False)
