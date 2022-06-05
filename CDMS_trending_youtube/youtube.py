# import required packages
from dash import dcc
from dash import html
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


class YoutubeTrendsStats():
    def __init__(self, application = None):
        self.df = pd.read_pickle('CDMS_trending_youtube/data/df_youtube.pkl')
        self.figure = self.create_figure(self.df)
        self.other_figure = self.create_figure2(self.df)

        # page layout
        self.app = application#dash.Dash()

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
        return fig

    # define figure creation function
    def create_figure(self,result):
        dates = self.divide_dates("2020-08-11", "2022-03-22", 12)

        # make list of continents
        countries = result['country'].unique()

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
    yt.app.run(port=8055)
