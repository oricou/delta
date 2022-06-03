import numpy as np
import pandas as pd


class Dataset:
    calls = None
    weather = None


def remove_outliers(x, standardize=False):
    data = x.fillna(method='ffill').fillna(method='backfill')
    data = data.where(np.abs((data - data.mean()) / data.std()) <= 2, np.nan)
    data = data.fillna(method='ffill').fillna(method='backfill')

    if standardize:
        return (data - data.min()) / (data.min() - data.max())

    return data


def load_calls_correlation_data():
    if Dataset.calls is None:
        Dataset.calls = pd.read_pickle("MDMR_NYPDCallsMeteoNY/data/NYPD_calls.pkl")

    return Dataset.calls


def load_weather_data():
    if Dataset.weather is None:
        Dataset.weather = pd.read_pickle("MDMR_NYPDCallsMeteoNY/data/weather.pkl")

    return Dataset.weather
