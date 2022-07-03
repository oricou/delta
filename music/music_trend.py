# import required packages
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px

d1 = "\u3131"
f1 = "\u3163"

d2 = "\uAC00"
f2 = "\uAF00"

d3 = "\uB000"
f3 = "\uBFE1"

d4 = "\uC058"
f4 = "\uCFFC"

d5 = "\uD018"
f5 = "\uD79D"

d6 = "\u3181"
f6 = "\uCB4C"


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
list_country = ["Brésil", "Canada", "Allemagne", "France",
        "Royaume-uni", "Inde", "Japon", "Corée", "Méxique", "Russier", "US"]
list_country_kor = ["Brésil", "Canada", "Allemagne", "France",
        "Royaume-uni", "Inde", "Japon", "Méxique", "Russier", "US"]

def load_data(list_file, list_country):
    datas = pd.DataFrame()
    for i in range(len(list_file)):
        data = pd.read_csv(list_file[i], sep=',')
        data['country'] = list_country[i]
        datas = pd.concat([datas, data])
    return datas

def is_korean(word):
    l = []
    for j in word:
        for i in j:
            if ord(i) >= ord(d1) and ord(i) <= ord(f1):
                l.append(j)
            if ord(i) >= ord(d2) and ord(i) <= ord(f2):
                l.append(j)
            if ord(i) >= ord(d3) and ord(i) <= ord(f3):
                l.append(j)
            if ord(i) >= ord(d4) and ord(i) <= ord(f4):
                l.append(j)
            if ord(i) >= ord(d5) and ord(i) <= ord(f5):
                l.append(j)
    return l

def ratio(list_country_kor, datas_year):
    ratio = []
    for country in list_country_kor:
        country_data = datas_year[datas_year.country == country]
        country_music = country_data[country_data.categoryId == 'Music']
        country_korean = is_korean(country_music.title)
        ratio.append(len(country_korean) * 100 / len(country_music))
    return ratio

# define figure creation function
def create_figure(result, list_country_kor):
    datas = result
    datas.trending_date = pd.to_datetime(datas.trending_date)
    datas['year'] = pd.DatetimeIndex(datas['trending_date']).year

    datas_2020 = datas[datas.year == 2020]
    datas_2021 = datas[datas.year == 2021]
    datas_2022 = datas[datas.year == 2022]

    ratio_2020 = ratio(list_country_kor, datas_2020)
    ratio_2021 = ratio(list_country_kor, datas_2021)
    ratio_2022 = ratio(list_country_kor, datas_2022)

    df = pd.DataFrame(index = list_country_kor)
    df['2020'] = ratio_2020
    df['2021'] = ratio_2021
    df['2022'] = ratio_2022

    fig = px.scatter(df, size=df*5, hover_name=df.index, 
    title='<b>Pourcentage de musique coréenne en tendance sur le total de musique en tendance pour chaque pays<b>',
        opacity = 0.6, labels={
                     "value": "Ratio in %",
                     "index": "Country",
                     "variable": "Year"
                 })
    fig.update_layout(
        title_font_size=22,
        font_family="Serif",
        title_font_family="Times New Roman",
        title_font_color="black"
    )
    fig.update_xaxes(title_font_family="Serif")
    return fig

# define dataframe creation function
def create_dataframe():

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

def divide_dates(start, end, N):
    test_date1 = datetime.strptime(start, '%Y-%m-%d')
    test_date2 = datetime.strptime(end, '%Y-%m-%d')
    temp = []
    diff = ( test_date2 - test_date1) // N
    for idx in range(0, N+1):
        temp.append((test_date1 + idx * diff).strftime("%Y-%m-%d"))
            # format
    return temp

def filter_dates(result, start_date, end_date):
    after_start_date = result["trending_date"] >= start_date
    before_end_date = result["trending_date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = result.loc[between_two_dates]
    return filtered_dates


# call figure and dataframe functions
df = create_dataframe()
figure = create_figure(df, list_country_kor)



# page layout
app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div(children=[
        html.H3(children='Évolution des proportions des catégories youtube en tendances dans le monde'),

        html.Div(dcc.Graph(id = 'main-graph',
                            figure = figure)),

    ], style={'display': 'inline-block', 'vertical-align': 'top'}),

])

if __name__ == "__main__":
    app.run_server(debug=True, port=8057)