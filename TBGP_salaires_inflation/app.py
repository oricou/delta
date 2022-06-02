from click import style
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import json
import os

path = '.' if __name__ == '__main__' else 'TBGP_salaires_inflation'

class SalaryInflation():
    def __init__(self, application = None):
        self.df = pd.read_pickle(f'{path}/data/dataframe.pkl') if os.path.exists(f'{path}/data/dataframe.pkl') else None
        self.geodata = json.load(open(f'{path}/data/europe.geojson')) if os.path.exists(f'{path}/data/europe.geojson') else None
        if not self.df is None:
            self.years = self.df.year.unique().astype('datetime64[Y]').astype(int) + 1970
            self.main_layout = html.Div(children=[
                html.H3(children='Comparaison salaire / inflation en Europe',
                    style={'textAlign': 'center'}),
                html.Div([dcc.Graph(id='tbgp-si-map'),

                    dcc.Markdown("""
                        La couleur représente le ratio entre le salaire médian de l'année choisie
                        et le salaire estimé selon le taux d'inflation et le salaire médian de référénce.

                        Les couleurs vers le rouge indiquent donc une perte de pouvoir d'achat, tandis que les couleurs vers le bleu
                        indiquent une hausse et le jaune indique un maintien.

                        L'année de référence et l'année à comparer peuvent être changés avec la barre ci-dessous.

                        Si les données de l'année de référence ou l'année à comparer n'existent pas pour un pays, il ne sera pas affiché sur la carte.
                        """),

                    html.Div(id='tbgp-si-year', style={'textAlign': 'center'})], style={'display': 'inline', 'justifyContent': 'center', 'width': '80%'}),

                dcc.RangeSlider(
                    id='tbgp-si-year-filter-slider',
                    min=self.years[0],
                    max=self.years[-1],
                    step=1,
                    pushable=1,
                    value=[2006, 2018],
                    marks={str(year): str(year)
                        for year in range(self.years[0], self.years[-1]+1, 5)}
                    ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='tbgp-si-graph',
                            style={'width': '85%', 'display': 'inline-block'}),
                        html.Div([
                            html.Button('Union Européenne', id='tbgp-si-europe_button', style={'width': '100%'}),
                            html.Div(html.U('Sexe :'), style={'padding-top': '10%'}),
                            dcc.RadioItems(id='tbgp-si-sex', options=[
                                {'label': 'Total', 'value': 'T'},
                                {'label': 'Hommes', 'value': 'M'},
                                {'label': 'Femmes', 'value': 'F'},
                                ], value='T', labelStyle={'display': 'block'}),
                            html.Div(html.U('Age :'), style={'padding-top': '5%'}),
                            dcc.RadioItems(id='tbgp-si-age', options=[
                                {'label': 'Total', 'value': 'TOTAL'},
                                {'label': 'Plus de 65 ans', 'value': 'Y_GE65'},
                                {'label': '50-64 ans', 'value': 'Y50-64'},
                                {'label': '25-49 ans', 'value': 'Y25-49'},
                                {'label': '16-24 ans', 'value': 'Y16-24'},
                                ], value='TOTAL', labelStyle={'display': 'block'}),
                            ], style={'width': '15%', 'display': 'block', 'padding-left': '1%' }),
                        ], style={'display': 'flex', 'justifyContent': 'center', }),
                    html.Div('* Salaire attendu si on prend uniquement l\'évolution de l\'inflation en compte'),
                    html.Br()
                    ]),
                dcc.Markdown("""
                    Ce projet montre l'évolution du salaire médian en Europe par rapport
                    à l'inflation. Notre méthode est simple : nous prenons une année de
                    référence, puis nous multiplions le salaire médian de cette année
                    par le taux d'inflation. La comparaison du salaire médian réel avec
                    celui estimé par l'inflation nous donne une estimation du gain ou de
                    la perte de pouvoir d'achat des habitants du pays en question.

                    La carte est interactive : cliquer sur un pays permet de mettre à
                    jour le graphique selon les statistiques de ce pays.

                    Le graphique affiche les statistiques de l'Union Européenne par
                    défaut. Un bouton est à votre disposition si vous voulez afficher
                    les stats de cette dernière sans recharger la page.

                    Vous pouvez également isoler les statistiques selon l'âge et le
                    sexe.

                    Enfin, changer l'année de référence pour l'inflation et l'année à comparer avec le slider
                    change également le graphique.

                    Observations :
                    * Les courbes sont toujours similaires selon les sexes, nous
                    remarquons juste que les valeurs sont généralement plus faibles pour les femmes.
                    * Il faut faire attention au fait que les plus de 65 ans en 2020 ne
                    sont pas les mêmes qu'en 1995. Ce biais doit être pris en compte
                    avant de tirer des conclusions de ces courbes.
                    * La crise de 2008 ne semble pas avoir trop affecté le rapport entre salaire médian et
                    l'inflation en Union Européenne, sauf au Royaume-Uni.

                    ### A propos

                    * Sources :
                        * [Le salaire médian en Europe selon l'âge et le sexe](https://ec.europa.eu/eurostat/fr/web/products-datasets/-/ILC_DI03) par Eurostat
                        * [L'évolution annuelle de l'inflation depuis 1995](https://data.oecd.org/fr/price/inflation-ipc.htm) par l'OCDE
                    * (c) 2022 Guillaume POISSON et Théo BACHIR
                    """),
            ])
        else:
            self.main_layout = dcc.Markdown('You need to fetch the data first.\n Please take a look at "TBGP_salaires_inflation/README.md" for more information.')

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        if not self.df is None:
            self.app.callback(
                    dash.dependencies.Output('tbgp-si-map', 'clickData'),
                    dash.dependencies.Input('tbgp-si-europe_button', 'n_clicks'))(self.set_ue)
            self.app.callback(
                dash.dependencies.Output('tbgp-si-year', 'children'),
                dash.dependencies.Input('tbgp-si-year-filter-slider', 'value'))(self.update_year)

            self.app.callback(
                dash.dependencies.Output('tbgp-si-map', 'figure'),
                dash.dependencies.Input('tbgp-si-year-filter-slider', 'value'))(self.update_map)

            self.app.callback(
                dash.dependencies.Output('tbgp-si-graph', 'figure'),
                [dash.dependencies.Input('tbgp-si-map', 'clickData'),
                    dash.dependencies.Input('tbgp-si-sex', 'value'),
                    dash.dependencies.Input('tbgp-si-age', 'value'),
                    dash.dependencies.Input('tbgp-si-year-filter-slider', 'value')])(self.update_graph)


    def set_ue(self, n):
        return None

    def update_year(self, years):
        return f'Années: {years[0]} - {years[1]}'

    def print_hover(self, hover):
        if hover is None:
            return 'EU27_2020'
        return hover['points'][0]['location'] if hover['points'][0]['location'] != 'UK' else 'GB'

    def update_map(self, years):
        dt0, dt1 = np.datetime64(int(years[0]) - 1970, 'Y'), np.datetime64(int(years[1]) - 1970, 'Y')

        data = self.df[(self.df.year == dt1) & (self.df.age == 'TOTAL') & (
            self.df.sex == 'T')][['country', 'cumulative_prod', 'wages_value']].set_index('country')

        # Wages within the time period
        base_values = self.df[(self.df.age == 'TOTAL') & (self.df.sex == 'T') & (self.df.year >= dt0) & (self.df.year <= dt1)].groupby('country').first()['wages_value']
        
        # Cumulative inflation of the reference year
        base_inflation = self.df[(self.df.year == dt0) & (self.df.age == 'TOTAL') & (
            self.df.sex == 'T')][['country', 'cumulative_prod']].set_index('country').rename(columns={'cumulative_prod' : 'base_inflation'})
        
        data = base_inflation.join(data, how='inner')

        # Ratio between the median wages of the compared year and the predicted median wages using the inflation
        data['Ratio'] = np.round(data['wages_value'] / (base_values * (data['cumulative_prod'] / data['base_inflation'])), 2)

        fig = px.choropleth_mapbox(data, geojson=self.geodata,
                                   locations=data.index, featureidkey='properties.ISO2',  # join keys
                                   color='Ratio', color_continuous_scale='rdylbu',
                                   range_color=(0,2),
                                   mapbox_style='carto-positron',
                                   zoom=3, center={'lat': 52, 'lon': 10},
                                   opacity=0.5,
                                   )
        fig.update_layout(
            title=f'{years}',
            margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
            hovermode='closest',
            showlegend=False,
        )

        return fig

    def update_graph(self, hover, sex, age, years):
        country = self.print_hover(hover)
        country_df = self.df[(self.df.country == country) &
                             (self.df.sex == sex) &
                             (self.df.age == age) &
                             (self.df.year >= np.datetime64(int(years[0]) - 1970, 'Y'))]
        
        # Compute the boundaries
        min_year = np.datetime64(country_df.year.iloc[0]).astype('datetime64[Y]').astype(int) + 1970
        max_year = max(min_year + 1, years[1])
        
        # Keep only values within the time period
        country_df = country_df[country_df.year <= np.datetime64(int(max_year) - 1970, 'Y')]

        # The wages of the reference year
        wages = country_df.wages_value.iloc[0]
        # The cumulative inflation of the reference year
        base_inflation = country_df.cumulative_prod.iloc[0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=country_df.year, y=np.round(country_df.wages_value, 0), mode='lines', name='Salaire réel'))
        fig.add_trace(go.Scatter(x=country_df.year, y=np.round(country_df.cumulative_prod / base_inflation * wages, 0), mode='lines', name='Inflation*'))
        fig.update_layout(
            title = 'Évolution du salaire médian comparé à l\'inflation depuis ' + f'{min_year}' + '.<br>Lieu : ' + country_name[country],
            title_xanchor = 'auto',
            title_pad = { 't': 0, 'b': 0, 'l': 0, 'r': 0},
            height=450,
            hovermode='x unified',
            legend = {'title': 'Courbes'},
            xaxis_title='Année',
            yaxis_title='Salaire médian (€)',
        )
        return fig

    def run(self, debug=False, port='8000'):
        self.app.run_server(host='0.0.0.0', debug=debug, port=port)


country_name = {
    'AT': 'Autriche',
    'BE': 'Belgique',
    'CZ': 'République tchèque',
    'DK': 'Danemark',
    'FI': 'Finlande',
    'FR': 'France',
    'DE': 'Allemagne',
    'GR': 'Grèce',
    'HU': 'Hongrie',
    'IS': 'Islande',
    'IE': 'Irlande',
    'IT': 'Italie',
    'LU': 'Luxembourg',
    'NL': 'Pays-Bas',
    'NO': 'Norvège',
    'PL': 'Pologne',
    'PT': 'Portugal',
    'SK': 'Slovaquie',
    'ES': 'Espagne',
    'SE': 'Suède',
    'TR': 'Turquie',
    'GB': 'Royaume-Unis',
    'EE': 'Estonie',
    'SI': 'Slovénie',
    'LV': 'Lettonie',
    'LT': 'Lituanie',
    'EU27_2020': 'Union Européenne'
}

if __name__ == '__main__':
    si = SalaryInflation()
    si.run(port='8045')
