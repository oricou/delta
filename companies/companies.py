import urllib.request
import os
import zipfile

import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.express as px

# config to download data
base_url = 'https://www.insee.fr'
url_creation = '/fr/statistiques/series/csv/famille/102722714'
url_destruction = '/fr/statistiques/series/csv/famille/102773703'
filename_creation = 'creation_entreprise'
filename_destruction = 'destruction_entreprise'
compression_extension = ".zip"
base_path = 'data/'
data_path = 'companies/data/'


class FrenchCompaniesStats:

    @staticmethod
    def __download_compressed_data():
        urllib.request.urlretrieve(base_url + url_creation, base_path + filename_creation + compression_extension)
        urllib.request.urlretrieve(base_url + url_destruction, base_path + filename_destruction + compression_extension)

    @staticmethod
    def __unzip_data():
        folders = [filename_creation, filename_destruction]
        for folder in folders:
            os.mkdir(data_path + folder)
            with zipfile.ZipFile(base_path + folder + compression_extension, 'r') as zip_ref:
                zip_ref.extractall(data_path + folder)

    @staticmethod
    def prepare_data():
        if not os.path.exists(data_path):
            os.mkdir(data_path)
            print(f"Downloading data for FrenchCompaniesStats from {base_url}")
            FrenchCompaniesStats.__download_compressed_data()
            print(f"Extracting data for FrenchCompaniesStats from {base_path} to {data_path}")
            FrenchCompaniesStats.__unzip_data()
        else:
            print(f"Data for FrenchCompaniesStats is already available. No need to download it again.")

    @staticmethod
    def __load_as_dataframe(file: str):
        return pd.read_csv(data_path + file, sep=";")

    def __clean_data(self):
        pass

    def __init__(self, application=None):

        # downloading and extracting the data
        FrenchCompaniesStats.prepare_data()

        # loading dataframes
        self.month_creations = FrenchCompaniesStats.__load_as_dataframe(
            filename_creation + "/valeurs_mensuelles.csv"
        )
        self.tri_creations = FrenchCompaniesStats.__load_as_dataframe(
            filename_creation + "/valeurs_trimestrielles.csv"
        )
        self.year_creations = FrenchCompaniesStats.__load_as_dataframe(
            filename_creation + "/valeurs_annuelles.csv"
        )

        self.month_destructions = FrenchCompaniesStats.__load_as_dataframe(
            filename_destruction + "/valeurs_mensuelles.csv"
        )
        self.tri_destructions = FrenchCompaniesStats.__load_as_dataframe(
            filename_destruction + "/valeurs_trimestrielles.csv"
        )
        self.year_destructions = FrenchCompaniesStats.__load_as_dataframe(
            filename_destruction + "/valeurs_annuelles.csv"
        )

        self.periodicity = 1;
        self.styles = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"];

        self.main_layout = html.Div(children=[
            html.H3(children="Evolution de la création et de la destruction d'entreprises en France"),
            html.Div([dcc.Graph(id='comp-main-graph'), ], style={'width': '100%', }),
            html.Div([
                html.Div([html.Div('Style du Graphique'),
                          dcc.Dropdown(
                              id='comp-graph_style',
                              options=[{'label': i, 'value': i} for i in self.styles],
                              value="seaborn",
                          ),
                          ], style={'width': '6em'}),
                html.Div([html.Div('Periodicité'),
                          dcc.RadioItems(
                              id='comp-periodicity',
                              options=[{'label': 'Annuelle', 'value': 0},
                                       {'label': 'Trimestrielle', 'value': 1},
                                       {'label': 'Mensuelle ', 'value': 2}],
                              value=1,
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '9em', 'margin-left': '2em'}),
                html.Div([html.Div('Échelle'),
                          dcc.RadioItems(
                              id='comp-xaxis',
                              options=[{'label': 'Linéaire', 'value': "linear"},
                                       {'label': 'Logarithmique', 'value': "logarithmic"}, ],
                              value="linear",
                              labelStyle={'display': 'block'},
                          )
                          ],style={'width': '15em', 'margin-left':"2em"} ),
            ], style={
                            'padding': '10px 50px',
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
        ])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('comp-main-graph', 'figure'),
            [
                dash.dependencies.Input('comp-periodicity', 'value'),
                dash.dependencies.Input('comp-xaxis', 'value'),
                dash.dependencies.Input('comp-graph_style', 'value'),
            ]
        )(self.update_graph)

    def __get_yearly_dataframe(self):
        years = list(map(lambda y: str(y), [i for i in range(1987, 2016)]))
        df_creation = self.year_creations[years].iloc[[0]].transpose()
        df_destruction = self.year_destructions[years].iloc[[0]].transpose()
        df = pd.concat([df_creation, df_destruction], axis=1, join='inner')
        df.columns = ["creation", "destruction"]
        return df

    def __get_monthly_dataframe(self):
        def __flat_map(f, values):
            out = []
            for val in values:
                out.extend(f(val))
            return out

        def get_months_of_year(year):
            return [f"{year}-{str(i).zfill(2)}" for i in range(1, 12)]

        pretransformed_dataframes = [(self.month_creations, 0), (self.month_destructions, 582)]
        transformed_dataframes = []
        for pre_df, row_for_total in pretransformed_dataframes:
            years = list(map(lambda y: str(y), [i for i in range(2000, 2021)]))
            months = __flat_map(get_months_of_year, years)
            monthly_reports = []
            for month in months:
                monthly_reports.append(pre_df[month].iloc[[row_for_total]])
            transformed_dataframes.append(pd.concat(monthly_reports, axis=1, join='inner').transpose())

        df = pd.concat(transformed_dataframes, axis=1, join='inner')
        df.columns = ["creation", "destruction"]
        return df

    def __get_quaterly_dataframe(self):
        def __flat_map(f, values):
            out = []
            for val in values:
                out.extend(f(val))
            return out

        def get_quaters_of_year(year):
            return [f"{year}-T{i}" for i in range(1, 5)]

        pretransformed_dataframes = [(self.tri_creations, 2354), (self.tri_destructions, 548)]
        transformed_dataframes = []
        for pre_df, row_for_total in pretransformed_dataframes:
            years = list(map(lambda y: str(y), [i for i in range(2000, 2015)]))
            quaters = __flat_map(get_quaters_of_year, years)
            quaterly_reports = []
            for quater in quaters:
                quaterly_reports.append(pre_df[quater].iloc[[row_for_total]])
            transformed_dataframes.append(pd.concat(quaterly_reports, axis=1, join='inner').transpose())

        df = pd.concat(transformed_dataframes, axis=1, join='inner')
        df.columns = ["creation", "destruction"]
        return df

    def update_graph(self, periodicity, xaxis_type='linear', graph_style='seaborn'):
        if periodicity == 0:
            df = self.__get_yearly_dataframe()
        elif periodicity == 1:
            df = self.__get_quaterly_dataframe()
        else:
            df = self.__get_monthly_dataframe()

        fig = px.line(df, template=graph_style)
        fig.add_scatter(mode='lines', name="des", text="z", hoverinfo='x+y+text')

        x_title = ["Année", "Trimestre", "Mois"]
        y_title = ["Nombre d'entreprises"] * 3

        fig.update_layout(
            xaxis=dict(title=x_title[periodicity]),
            yaxis=dict(title=y_title[periodicity], type='linear' if xaxis_type == 'linear' else 'log', ),
            height=450,
            hovermode='closest',
            legend={'title': 'Légende'},
        )
        return fig


if __name__ == '__main__':
    data_path = 'data/'
    nrg = FrenchCompaniesStats()
    nrg.app.run_server(debug=True, port=8052)
