import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du


def load_data(filename):
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    print(df)
    print("Number of NaN : ", df.isna().sum().sum())
    return df


class Vaccinations():

    def __init__(self, filename):
        df = load_data(filename)


if __name__ == '__main__':
    Vaccinations("data/vaccinations.csv")
