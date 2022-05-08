import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from urllib.request import urlopen
import json
import geopandas as gpd
from Levenshtein import ratio
import re


def to_str(n):
    try:
        return "0" + str(n) if n < 10 else str(n)
    except:
        return n


class Anthroponymie():
    def __init__(self, application=None):
        url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
        self.dpts_json = json.loads(urlopen(url).read())
        gdf = gpd.GeoDataFrame.from_features(self.dpts_json["features"])
        df_name = gdf.drop(columns=['geometry']).set_index("code")
        name_map = df_name.to_dict()['nom']

        df = pd.read_csv('PSJCD_Anthroponymie/data/nomsParDpt.txt', sep='\t', lineterminator='\n')

        df["DEP"] = df["DEP"].map(to_str)
        df.rename(columns={"NOM": "Nom", "DEP": "Dpt", "_1991_2000\r": "_1991_2000"}, inplace=True)
        dpt_arr = np.unique(df.Dpt.to_numpy(dtype=str))
        df = df[[dep in dpt_arr[:-6] for dep in df['Dpt']]]
        dpt_names = df.Dpt.map(name_map)
        df.insert(2, "Nom_Dpt", dpt_names)
        df.columns = df.columns.str.replace(r'^_', '')

        self.df = df
        self.decades = [str(i) + '_' + str(i + 9) for i in range(1891, 2001, 10)]
        self.funcs = [self.extract_exact_names, self.extract_composed_names, self.extract_levenstein,
                      self.extract_all_names]

        self.main_layout = html.Div(children=[
            html.H3(children='Anthroponymie par département'),
            html.Div([dcc.Graph(id='atr-graph'), ], style={'width': '100%', 'min-height': '50vh'}),
            html.Div([
                html.Div([html.Div('Recherche'),
                          dcc.Input(
                              id="atr-name",
                              type="text",
                              placeholder="Votre nom",
                              value="",
                          )
                          ], style={'marginRight': '10px'}),
                html.Div([html.Div('Décennie'),
                          dcc.Slider(0, len(self.decades) - 1,
                                     step=None,
                                     marks={i: dec for i, dec in enumerate(self.decades)},
                                     value=0,
                                     id='atr-decade',
                                     included=False
                                     )]),
                html.Div([html.Div('Fonction de reconnaissance'),
                          dcc.RadioItems(
                              id='atr-func_id',
                              options=[{'label': "Nom exact", 'value': 0},
                                       {'label': "Avec noms composés", 'value': 1},
                                       {'label': "Avec noms proches", 'value': 2},
                                       {'label': "Avec noms proches + composés", 'value': 3}],
                              value=0,
                              labelStyle={'display': 'block'},
                          )
                          ], style={'marginRight': '10px'}),
            ]),
            html.Br(),
            dcc.Markdown("""
        La carte est interactive. En passant la souris sur les départements colorés vous avez une infobulle.
        Vous retrouverez les noms similaires à celui que vous avez choisi pour chaque départements. 
        En utilisant la souris, on peut zoomer dans la carte et se déplacer dessus, réinitialiser, etc.

        #### À propos

        * Sources :
            * https://www.insee.fr/fr/statistiques/3536630
            * https://france-geojson.gregoiredavid.fr/repo/departements.geojson
        * (c) 2022 Pejman Samieyan, Jules Coquel-Doucet
        """)
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('atr-graph', 'figure'),
            [dash.dependencies.Input('atr-name', 'value'),
             dash.dependencies.Input('atr-decade', 'value'),
             dash.dependencies.Input('atr-func_id', 'value')])(self.update_graph)

    def extract_exact_names(self, check: str):
        return self.df[self.df['Nom'] == check].copy()

    def extract_composed_names(self, check: str):
        return self.df[[re.search(r"^([A-Z]+-)?" + re.escape(check) + "(-[A-Z]+)?$", nom) is not None for nom in
                        self.df['Nom']]].copy()

    def extract_levenstein(self, check: str):
        return self.df[[ratio(nom, check) > 0.9 for nom in self.df['Nom']]].copy()

    def extract_all_names(self, check: str):
        return pd.concat([self.df[[ratio(nom, check) > 0.9 for nom in self.df['Nom']]],
                          self.df[
                              [re.search(r"^([A-Z]+-)?" + re.escape(check) + "(-[A-Z]+)?$", nom) is not None for nom in
                               self.df['Nom']]]]
                         ).drop_duplicates().copy()

    def get_df(self, name, func):
        df_name = func(name)
        cols = self.df.columns.tolist()
        cols = cols[2:]
        col_dict = {cols[0]: lambda x: x.iloc[0] if x.shape[0] > 0 else 0}
        for i, col in enumerate(cols):
            if i > 0:
                col_dict.update({col: sum})
        ret_df = df_name.groupby(by='Dpt').agg(col_dict)
        name_dep_arr = df_name[['Nom', 'Dpt']].to_numpy(dtype=str)

        dico = dict(
            {key: ", ".join(name_dep_arr[name_dep_arr[:, 1] == key][:, 0]) for key in np.unique(name_dep_arr[:, 1])})

        ret_df['Noms'] = ret_df.index.map(dico)
        cols = ret_df.columns.tolist()
        ret_df = ret_df[cols[-1:] + cols[:-1]]
        if len(ret_df.index) == 0:
            null_dic = {'Noms': name, 'Nom_Dpt': 'Paris'}
            for i in range(1891, 2001, 10):
                null_dic.update({str(i) + '_' + str(i + 9): 0})
            null_df = pd.DataFrame(null_dic, index=[75])
            ret_df = pd.concat([ret_df, null_df])
        return ret_df

    def update_graph(self, name: str, dec: int, func_id: int):
        name = name.upper()
        decade_str = self.decades[dec]
        years = decade_str.split('_')
        fig_df = self.get_df(name, self.funcs[func_id])

        fig = px.choropleth_mapbox(fig_df,
                                   geojson=self.dpts_json,
                                   locations=fig_df.index,
                                   featureidkey="properties.code",
                                   color=decade_str,
                                   hover_data=["Nom_Dpt", 'Noms', decade_str],
                                   center={"lat": 46.79491, "lon": 3.03206},
                                   mapbox_style="open-street-map",
                                   labels={decade_str: 'Nombre par département'},
                                   opacity=0.65,
                                   zoom=5,
                                   title=f"Entre {years[0]} et {years[1]}",
                                   height=600)
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig


if __name__ == '__main__':
    atr = Anthroponymie()
    atr.app.run_server(debug=True, port=8051)
