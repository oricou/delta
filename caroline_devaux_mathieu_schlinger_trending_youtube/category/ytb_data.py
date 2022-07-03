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

def ratio(list_country_kor, datas_year):
    ratio = []
    for country in list_country_kor:
        country_data = datas_year[datas_year.country == country]
        country_music = country_data[country_data.categoryId == 'Music']
        country_korean = is_korean(country_music.title)
        ratio.append(len(country_korean) * 100 / len(country_music))
    return ratio

list_country = ["Brésil", "Canada", "Allemagne", "France",
    "Royaume-Uni", "Inde", "Japon", "Corée", "Méxique", "Russie", "US"]
list_country_kor = ["Brésil", "Canada", "Allemagne", "France",
    "Royaume-Uni", "Inde", "Japon", "Méxique", "Russie", "US"]

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
    
def load_data(list_file, list_country):
    datas = pd.DataFrame()
    for i in range(len(list_file)):
        data = pd.read_csv(list_file[i], sep=',')
        data['country'] = list_country[i]
        datas = pd.concat([datas, data])
    return datas

class YoutubeTrendsStats():
    def __init__(self, application = None):
        self.df = self.create_dataframe()
        self.figure = self.create_figure(self.df)
        self.other_figure = self.create_figure2(self.df)

        # page layout
        self.app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

        div_content = html.Div(children=[
                # html.H3(children='Évolution des proportions des catégories youtube en tendances dans le monde'),

                html.Div(dcc.Graph(id = 'main-graph',
                                    figure = self.figure)),
                # html.H3(children='Pourcentage de musique coréenne en tendance sur le total de musique en tendance pour chaque pays'),
                html.Div(dcc.Graph(id = 'second-graph',
                                    figure = self.other_figure)),
                html.Br(),
                dcc.Markdown("""
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
                
                Notes :
                   * La catégorie Entertainement est la plus en tendance dans la plupart des pays.
                   * Entre le 13/04/20021 et le 01/06/2021, la catégorie Gaming représentait 13,3%/ des tendances en France
                   * On peut voir que la musique Coréenne représente la majorité des musiques de plusieurs pays.
                   

                #### À propos

                * Sources : 
                   * https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset?select=FR_youtube_trending_data.csv
                """)

            ])#, style={'display': 'inline-block', 'vertical-align': 'top'})

        self.app.layout = div_content
        self.main_layout = div_content

    def create_figure2(self, datas):
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

        y0 = np.array(df['2020'])
        fig = px.scatter(df, size=y0*5, hover_name=df.index,
            title='Pourcentage de musique coréenne en tendance sur le total de musique en tendance pour chaque pays',
            opacity = 0.6, labels={
                            "value": "Ratio in %",
                            "index": "Country",
                            "variable": "Year"
                        })
        #fig.update_layout(
        #    title_font_size=22,
        #    font_family="Serif",
        #    title_font_family="Times New Roman",
        #    title_font_color="black"
        #)
        #fig.update_xaxes(title_font_family="Serif")
        return fig

    # define figure creation function
    def create_figure(self,result):
        dates = self.divide_dates("2020-08-11", "2022-03-22", 12)

        # make list of continents
        countries = result['country'].unique()
        print(countries)

        domains = [
            {'x': [0.0, 0.25], 'y': [0.0, 0.33]},
            {'x': [0.0, 0.25], 'y': [0.33, 0.66]},
            {'x': [0.0, 0.25], 'y': [0.66, 1.0]},
            {'x': [0.25, 0.5], 'y': [0.0, 0.33]},
            {'x': [0.25, 0.5], 'y': [0.33, 0.66]},
            {'x': [0.25, 0.5], 'y': [0.66, 1.0]},
            {'x': [0.5, 0.75], 'y': [0.0, 0.33]},
            {'x': [0.5, 0.75], 'y': [0.33, 0.66]},
            {'x': [0.5, 0.75], 'y': [0.66, 1.0]},
            {'x': [0.75, 1.0], 'y': [0.0, 0.33]},
            {'x': [0.75, 1.0], 'y': [0.33, 0.66]},
            {'x': [0.75, 1.0], 'y': [0.66, 1.0]}
        ]
        #countries = ["France", "Canada"]
        # make figure
        fig_dict = {
            "data": [],
            "layout": {},
            "frames": []
        }

        # fill in most of layout
        fig_dict["layout"]["title"] = "Évolution des proportions des catégories youtube en tendances dans le monde"
        fig_dict["layout"]["height"] = 700
        fig_dict["layout"]["hovermode"] = "closest"
        fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 1000, "redraw": True},
                                        "fromcurrent": True, "transition": {"duration": 300,
                                                                            "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        # make data
        i = 0
        for country in countries:
            res_filtered = self.filter_dates(result, dates[0], dates[1])
            pie = go.Pie(labels=res_filtered[res_filtered["country"] == country]["categoryId"], domain = domains[i], title=country, textinfo='none', hole=.6)
            fig_dict["data"].append(pie)
            i+=1

        # make frames
        for x in range(1,len(dates)-1):
            frame = {"data": [], "name": str(dates[x])}
            i = 0
            for country in countries:
                res_filtered = self.filter_dates(result, dates[x], dates[x+1])
                pie = go.Pie(labels=res_filtered[res_filtered["country"] == country]["categoryId"], domain = domains[i], title=country, textinfo='none', hole=.6)
                frame["data"].append(pie)
                i+=1
            fig_dict["frames"].append(frame)
            slider_step = {"args": [
                [dates[x]],
                {"frame": {"duration": 300, "redraw": True},
                "mode": "immediate",
                "transition": {"duration": 300}}
            ],
                "label": dates[x],
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)

        fig_dict["layout"]["sliders"] = [sliders_dict]

        fig = go.Figure(fig_dict)
        return fig

    def create_dataframe(self):
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
    
    def divide_dates(self, start, end, N):
        test_date1 = datetime.strptime(start, '%Y-%m-%d')
        test_date2 = datetime.strptime(end, '%Y-%m-%d')
        temp = []
        diff = ( test_date2 - test_date1) // N
        for idx in range(0, N+1):
            temp.append((test_date1 + idx * diff).strftime("%Y-%m-%d"))
                # format
        return temp

    def filter_dates(self, result, start_date, end_date):
        after_start_date = result["trending_date"] >= start_date
        before_end_date = result["trending_date"] <= end_date
        between_two_dates = after_start_date & before_end_date
        filtered_dates = result.loc[between_two_dates]
        return filtered_dates
        
    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == "__main__":
    yt = YoutubeTrendsStats()
    yt.run(port=8055)