import pandas as pd
import tarfile

# Paths to data.tar.gz of the 2 database
path_tarball = './TA_MG_SpotifyMusicPopularity/data/data.tar.gz'

# Name of files who will be created
paths = ["./TA_MG_SpotifyMusicPopularity/data/SpotifyFeatures.csv",
         "./TA_MG_SpotifyMusicPopularity/data/charts.csv"]

def get_data():
    my_tar = tarfile.open(path_tarball)
    my_tar.extractall('./TA_MG_SpotifyMusicPopularity/data')
    my_tar.close()

    df = pd.read_csv(paths[0])
    dfcharts = pd.read_csv(paths[1])
    
    # Ligne pour couper les dates dont on a pas besoin
    dfcharts = dfcharts.drop(dfcharts[dfcharts.date != "2021-11-30"].index)

    # Ligne pour réinitialiser l'index
    dfcharts.reset_index(inplace=True)

    # Ligne pour supprimer l'ancienne colonne d'index
    dfcharts = dfcharts.drop(columns=['index'])

    # Ligne pour enlever la typo sur un des genre de musique
    df.loc[df.genre == 'Children’s Music', 'genre'] = 'Children\'s Music'

    # Ligne pour harmoniser les 2 csv
    df = df.rename(columns={'artist_name':'artist', 'track_name':'title'})

    # Ligne pour réecrire la base données
    df.to_csv(paths[0])
    dfcharts.to_csv(paths[1])

if __name__ == '__main__':
    get_data()