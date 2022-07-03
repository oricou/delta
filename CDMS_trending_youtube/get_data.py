import pandas as pd
from zipfile import ZipFile
import os

os.environ['KAGGLE_USERNAME'] = "matthieuschlienger"
os.environ['KAGGLE_KEY'] = "1fae511f2e110e02b5ace27a55a50fec"

from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
api.dataset_download_files('rsrishav/youtube-trending-video-dataset', path="./tmp")
with ZipFile('./tmp/youtube-trending-video-dataset.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall('./tmp')

list_country = ["Brésil", "Canada", "Allemagne", "France",
    "Royaume-Uni", "Inde", "Japon", "Corée", "Méxique", "Russie", "US"]
list_country_kor = ["Brésil", "Canada", "Allemagne", "France",
    "Royaume-Uni", "Inde", "Japon", "Méxique", "Russie", "US"]

def load_data(list_file, list_country):
    datas = pd.DataFrame()
    for i in range(len(list_file)):
        data = pd.read_csv(list_file[i], sep=',')
        data['country'] = list_country[i]
        datas = pd.concat([datas, data])
    return datas

'''def create_dataframe():
    list_file = ["tmp/archive/BR_youtube_trending_data.csv",
        "tmp/archive/CA_youtube_trending_data.csv",
        "tmp/archive/DE_youtube_trending_data.csv",
        "tmp/archive/FR_youtube_trending_data.csv",
        "tmp/archive/GB_youtube_trending_data.csv",
        "tmp/archive/IN_youtube_trending_data.csv",
        "tmp/archive/JP_youtube_trending_data.csv",
        "tmp/archive/KR_youtube_trending_data.csv",
        "tmp/archive/MX_youtube_trending_data.csv",
        "tmp/archive/RU_youtube_trending_data.csv",
        "tmp/archive/US_youtube_trending_data.csv"]
'''
def create_dataframe():
    list_file = ["tmp/BR_youtube_trending_data.csv",
        "tmp/CA_youtube_trending_data.csv",
        "tmp/DE_youtube_trending_data.csv",
        "tmp/FR_youtube_trending_data.csv",
        "tmp/GB_youtube_trending_data.csv",
        "tmp/IN_youtube_trending_data.csv",
        "tmp/JP_youtube_trending_data.csv",
        "tmp/KR_youtube_trending_data.csv",
        "tmp/MX_youtube_trending_data.csv",
        "tmp/RU_youtube_trending_data.csv",
        "tmp/US_youtube_trending_data.csv"]

    data = load_data(list_file, list_country)
    data.drop(columns=['channelId', 'description','thumbnail_link','video_id'], inplace=True, axis=1)

    result = data.copy()
    result['publishedAt'] = pd.to_datetime(result['publishedAt'], format='%Y-%m-%d')
    replace_categories = { 2: 'Autos & Vehicles',
    1: 'Film & Animation',
    10: 'Music',
    15: 'Pets & Animals',
    17: 'Sports',
    18: 'Short Movies',
    19: 'Travel & Events',
    20: 'Gaming',
    21: 'Videoblogging',
    22: 'People & Blogs',
    23: 'Comedy',
    24: 'Entertainment',
    25: 'News & Politics',
    26: 'Howto & Style',
    27: 'Education',
    28: 'Science & Technology',
    29: 'Nonprofits & Activism'}

    df = result.replace({"categoryId": replace_categories})

    return df


youtube_df = create_dataframe()

os.mkdir("./data")

youtube_df.to_pickle("./data/df_youtube.pkl")
