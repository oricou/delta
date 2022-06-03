# Computes differences to see if there are high jumps in usage

import functools
import pandas as pd
import json
import plotly.graph_objects as go
from dash import dcc
from dash import html
import glob


files = sorted(glob.glob("data/velib/grouped_2022_03_11_*_[03]0_velib.csv") +
               ["data/velib/grouped_2022_03_12_00_00_velib.csv", "data/velib/grouped_2022_03_10_23_30_velib.csv"])
print(files)
print(len(files))

for i in range(len(files) - 1):
    file1 = files[i]
    file2 = files[i + 1]

    print(file2)

    data = file2.replace("data/velib/grouped_", "data/velib/diff_")

    df1 = pd.read_csv(file1, sep=";")
    df2 = pd.read_csv(file2, sep=";")

    df2["avail. bike"] -= df1["avail. bike"]

    df2.to_csv(data, sep=";", index_label=False, index=False)

out = pd.DataFrame({'hour': [], 'diff': []})
files = sorted(glob.glob("data/velib/diff_*"))

for i in range(len(files) - 1):
    df1 = pd.read_csv(files[i], sep=";")
    df2 = pd.read_csv(files[i + 1], sep=";")

    date = files[i + 1].replace('data/velib/diff_',
                                '').replace('_velib.csv', '')[8:]

    diff = (df1["avail. bike"].sum() - df2["avail. bike"].sum()).__abs__()
    out = pd.concat(
        [out, pd.DataFrame({'hour': [date], 'diff': [diff]})], ignore_index=True)


out.to_csv("data/velib/col_diff_velib.csv",
           sep=";", index_label=False, index=False)
