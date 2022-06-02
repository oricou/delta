import zipfile
import pandas as pd
import ast

def unzip_file(str) :
    zipfile.ZipFile(str, 'r').extractall("data/")

unzip_file("data/artists.zip")
unzip_file("data/album_ratings.zip")
unzip_file("data/tracks.zip")

s_artists = pd.read_csv("data/artists.zip", converters={2:ast.literal_eval})
s_artists = s_artists.rename(columns={"name":"artists"})

songs = pd.read_csv("data/tracks.zip")
songs.drop(songs[songs["popularity"] == 0].index, inplace = True)
songs.drop(columns=["time_signature", "tempo", "valence", "liveness", "instrumentalness", "acousticness", "speechiness", "mode", "loudness", "key", "energy", "duration_ms"], inplace=True)
songs.drop_duplicates(subset=["name", 'artists'], inplace=True)

songs['id_artists'] = songs['id_artists'].astype(str)
songs['id_artists'] = songs['id_artists'].apply(lambda x: (x[2:])[:-2])
songs['artists'] = songs['artists'].astype(str)
songs['artists'] = songs['artists'].apply(lambda x: (x[2:])[:-2])

df = pd.read_csv("data/album_ratings.zip")
df.rename(columns={"Artist": "artists"}, inplace=True)


        
        #Join entre les datasets
artists = df.merge(s_artists, how="inner", on = "artists")
artists = artists.dropna()
artists = artists.rename(columns={"id": "id_artists"})

artists = artists.sort_values(by= "followers", ascending=False)

Tracks = songs.merge(artists, how="inner", on = ["artists", "id_artists"])
Tracks.drop_duplicates(subset="name", inplace=True, ignore_index=True)
        
Tracks.sort_values(by="danceability", inplace=True, ascending=False)
        
        #ca fonctionne?!
songs_pays = pd.read_csv("data/songsbycountry.zip")
        
songs_pays.drop(songs_pays[songs_pays["Country"] == "Global"].index, inplace = True)
songs_pays.drop(columns= ["Continent", "Explicit", "Duration"], inplace=True)
songs_pays.rename(columns={"Title":"name", "Artists":"artists"}, inplace=True)

head_country = songs_pays[songs_pays["Rank"] == 1].reset_index()
head_country["index"] = head_country.index
        
songpopularity = songs_pays.merge(Tracks, how="inner", on=["artists", "name"])

songs.to_pickle("data/songs.pkl")
df.to_pickle("data/df.pkl")
artists.to_pickle("data/artists.pkl")
Tracks.to_pickle("data/Tracks.pkl")
songs_pays.to_pickle("data/songs_pays.pkl")
head_country.to_pickle("data/head_country.pkl")
songpopularity.to_pickle("data/songpopularity.pkl")