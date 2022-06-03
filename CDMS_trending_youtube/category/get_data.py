import pandas as pd

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

def create_dataframe():
    list_file = ["category/archive/BR_youtube_trending_data.csv",
        "category/archive/CA_youtube_trending_data.csv",
        "category/archive/DE_youtube_trending_data.csv",
        "category/archive/FR_youtube_trending_data.csv",
        "category/archive/GB_youtube_trending_data.csv",
        "category/archive/IN_youtube_trending_data.csv",
        "category/archive/JP_youtube_trending_data.csv",
        "category/archive/KR_youtube_trending_data.csv",
        "category/archive/MX_youtube_trending_data.csv",
        "category/archive/RU_youtube_trending_data.csv",
        "category/archive/US_youtube_trending_data.csv"]

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

youtube_df.to_pickle("./data/df_youtube.pkl")