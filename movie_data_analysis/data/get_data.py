import pandas as pd
import numpy as np
import csv

df = pd.read_csv("movie_data_analysis/data/movies_metadata.csv", dtype={'popularity': 'str'})

# remove entries where release date is na
df = df.dropna(subset=["release_date", "title"])

# drop useless columns (tagline ? belongs_to_collection ? runtime ?
df = df.drop(columns=["adult", "poster_path", "homepage", "video", "original_title", "belongs_to_collection"])

df["release_year"] = df["release_date"].str[:4]

# vote count 0 ?
# budget == 0 pour 36000 rows 


# PRODUCTION DE FILMS

section1 = df.drop(columns=["imdb_id", "runtime", "revenue", "vote_count", "vote_average", "status", "popularity", "tagline", "overview", "production_companies", "production_countries", "title", "spoken_languages", "release_date", "id", "original_language"])
section1.to_csv("movie_data_analysis/evolution_production/data/production.csv")

# CRITIQUE VS BUDGET

section2 = df.drop(columns=["id", "overview", "production_companies", "tagline", "spoken_languages", "production_countries", "imdb_id"])
section2 = section2.drop(section2[section2["budget"] == "0"].index)
section2.to_csv("movie_data_analysis/critique_budget/data/critique_budget.csv")

# POPULARITE ET THEME

section3 = df.drop(columns=["id", "imdb_id", "production_countries", "production_companies"])
section3 = section3.drop(section3[section3["budget"] == "0"].index)
section3 = section3.drop(section3[section3["revenue"] == 0].index)
section3.to_csv("movie_data_analysis/theme_popularite/data/theme_popularite.csv")

# PRODUCTION ET MONOPOLE

section4 = df.drop(columns=["genres", "id", "imdb_id", "overview", "tagline"])
section4 = section4.drop(section4[section4["budget"] == "0"].index)

companies = section4.copy()
companies = companies.drop(companies[companies["production_companies"] == "[]"].index)
companies = companies.drop(columns=["production_countries"])

countries = section4.copy()
countries = countries.drop(countries[countries["production_countries"] == "[]"].index)
countries = countries.drop(columns=["production_companies"])

companies.to_csv("movie_data_analysis/producteurs/data/entreprises_producteurs.csv")
countries.to_csv("movie_data_analysis/producteurs/data/pays_producteurs.csv")

# KEYWORD ET POPULARITE

section5 = df.drop(columns=["budget", "id", "imdb_id", "production_companies", "production_countries", "spoken_languages"])
section5.to_csv("movie_data_analysis/keywords_popularite/data/keywords_popularite.csv")