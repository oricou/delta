import pandas as pd
import requests
import json
import tqdm
import os

api_key = "8e62d30a01b0eeffec74723abe0e5e62"
url = "http://files.tmdb.org/p/exports/movie_ids_04_28_2022.json.gz"

target_path = "movie_ids_04_28_2022.json.gz"

response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(target_path, 'wb') as f:
        f.write(response.raw.read())

df = pd.read_json('./movie_ids_04_28_2022.json.gz', lines=True)
df = df[df["popularity"] > 10]

l = []
for i, row in tqdm.tqdm(df.iterrows()):
    movie_id = row["id"]
    URL = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    # sending get request and saving the response as response object
    r = requests.get(url=URL)

    # extracting data in json format
    data = r.json()
    l.append(data)

big_df = pd.DataFrame(l)
big_df.drop(
    columns=['adult', 'backdrop_path', 'belongs_to_collection', 'homepage', 'id', 'imdb_id', 'overview', 'poster_path',
             'production_companies', 'production_countries', 'runtime', 'spoken_languages', 'status', 'tagline',
             'title', 'video', 'success', 'original_language', 'status_code', 'status_message'], inplace=True)
big_df = big_df.explode('genres')
big_df['genres'] = big_df['genres'].apply(lambda x: x.get('name') if type(x) is dict else 'None')
big_df['release_date'] = pd.to_datetime(big_df['release_date'],format='%Y-%m-%d')
big_df['year'] = pd.DatetimeIndex(big_df['release_date']).year
big_df['year'] = pd.to_numeric(big_df['year'], errors='coerce')
big_df = big_df.dropna(subset=['year'])
big_df['year'] = big_df['year'].astype(int)
big_df['budget'] = big_df['budget'].astype(int)
big_df['popularity'] = big_df['popularity'].astype(int)
big_df['revenue'] = big_df['revenue'].astype(int)
big_df.drop(columns=['release_date'], inplace=True)
big_df = big_df.set_index('year')
big_df = big_df[big_df['genres'] != 'None']
os.remove('./movie_ids_04_28_2022.json.gz')
big_df.to_pickle("./movies_data.pkl")
