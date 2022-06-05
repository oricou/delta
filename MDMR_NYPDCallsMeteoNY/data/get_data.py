"""
This script allow us to generate the dataset needed for the project.
All the dataset are in the folder 'data'.

In this folder 'data', you can find:
	- NYPD_calls_{n}.csv.zip: These files contain all the information about the NYPD calls.
	https://data.cityofnewyork.us/Public-Safety/NYPD-Calls-for-Service-Historic-/d6zx-ckhd

	- weather.csv.zip: This file contains the data about the weather.
	https://meteostat.net/fr/place/us/new-york-city?t=2018-01-01/2020-12-31

	- NYPD_calls.pkl: This file contains all the data about the NYPD calls needed for this project.

	- weather.pkl: This file contains all the data about the weather in New-York needed for this project.

This script will create two files 'NYPD_calls.pkl' and 'weather.pkl'.
"""


import pandas as pd
import glob


def inside_outside(line: str) -> str:
    line = line.split("/")[-1]
    inside = ["RESIDENCE", "INSIDE", "DOMESTIC", "COMMERCIAL"]
    outside = ["OUTSIDE", "TRANSIT"]

    if any(ext in line for ext in inside):
        return "Intérieur"
    elif any(ext in line for ext in outside):
        return "Extérieur"
    return "Inconnu"


def generate_data_NYPD_calls(file_format: str, save_path: str) -> None:
    all_files = glob.glob(file_format)

    dataset = pd.concat(
        [
            pd.read_csv(
                file,
                parse_dates=["INCIDENT_DATE"],
                index_col=["INCIDENT_DATE"],
                usecols=["INCIDENT_DATE", "TYP_DESC", "CIP_JOBS"],
                compression="zip",
            )
            for file in all_files
        ]
    )

    dataset.index.name = "date"
    dataset = dataset.rename(columns={"TYP_DESC": "typDesc", "CIP_JOBS": "cipJobs"})
    dataset = dataset[dataset.cipJobs != "Non CIP"]

    dataset["desc"] = dataset.typDesc.apply(
        lambda x: x.split(":")[0].split(" (IN PROGRESS)")[0].capitalize()
    )
    dataset["place"] = dataset.typDesc.apply(lambda x: inside_outside(x).capitalize())
    dataset = dataset.drop(columns=["typDesc"])

    dataset.to_pickle(save_path)


def generate_data_weather(file_format: str, save_path: str) -> None:
    dataset = pd.read_csv(
        file_format, parse_dates=["date"], index_col=["date"], compression="zip"
    )

    dataset = dataset.drop(columns=["tsun", "wpgt"]).ffill()

    dataset.to_pickle(save_path)


def generate_data() -> None:
    generate_data_NYPD_calls("NYPD_calls_*.csv.zip", "NYPD_calls.pkl")
    generate_data_weather("weather.csv.zip", "weather.pkl")


if __name__ == "__main__":
    generate_data()
