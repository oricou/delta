import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from scipy import stats
from scipy import fft
import datetime

Y_AXIS_OPTIONS = [
  {'label' : 'Postive', 'value' : 'pos'},
  {'label' : 'Postive 7-jours', 'value' : 'pos_7j'},
  {'label' : 'Hospitalisés', 'value' : 'hosp'},
  {'label' : 'Réanimation', 'value' : 'rea'},
  {'label' : 'Décès à l’hôpital', 'value' : 'incid_dchosp'},
]

MONTHS_YEARS = {
  0 : '2020 May',
  1 : '2020 June',
  2 : '2020 July',
  3 : '2020 August',
  4 : '2020 September',
  5 : '2020 October',
  6 : '2020 November',
  7 : '2020 December',
  8 : '2021 January',
  9 : '2021 February',
  10 : '2021 March',
  11 : '2021 April',
  12 : '2021 May',
  13 : '2021 June',
  14 : '2021 July',
  15 : '2021 August',
  16 : '2021 September',
  17 : '2021 October',
  18 : '2021 November',
  19 : '2021 December',
  20 : '2022 January',
  21 : '2022 February',
  22 : '2022 March',
  23 : '2022 April',
  24 : '2022 May'
}
class CovidBasics():
    def __init__(self, application = None):
        # Main df
        self.df = pd.read_pickle('data/covid-all-stats-departments.pkl')

        # Sidescroll df
        self.month_year_df = self.df.reset_index()
        self.month_year_df['month'] = pd.to_datetime(self.month_year_df['date']).dt.month_name() 
        self.month_year_df['year'] = pd.to_datetime(self.month_year_df['date']).dt.year
        self.month_year_df = self.month_year_df.groupby(['year', 'month', 'lib_reg']).sum().reset_index()

        # 2021
        self.regions_2021 = self.df.reset_index()
        self.regions_2021['month'] = pd.to_datetime(self.regions_2021['date']).dt.month_name() 
        self.regions_2021['month_order'] = pd.to_datetime(self.regions_2021['date']).dt.month
        self.regions_2021['year'] = pd.to_datetime(self.regions_2021['date']).dt.year     
        self.regions_2021 = self.regions_2021[self.regions_2021.year == 2021].groupby(['lib_reg', 'month']).mean().reset_index()
        self.regions_2021 = self.regions_2021.sort_values('month_order')

        self.radio_options = [
          { 'label': reg, 'value': reg }
          for reg in self.df['lib_reg'].drop_duplicates().values
        ]
        self.radio_options.append({ 'label': 'France', 'value': 'France' })

        self.main_layout = html.Div(children=[
            html.H3(children='Covid Basics'),
            html.Div([ dcc.Graph(id='cvd-main-graph'), ], style={'width':'100%', }),
            html.Div([
              html.Div([ html.Div('Région'), dcc.Dropdown(id='cvd-region', 
                                      options=self.radio_options,
                                      value='Île-de-France')], style={'width': '15em', 'display': 'inline-block'}),
              html.Div([ html.Div('Y Axis'), dcc.RadioItems(id='cvd-yaxis', 
                                      options=Y_AXIS_OPTIONS,
                                      value='pos_7j')], style={'width': '15em', 'display': 'inline-block'}),
            ]),
            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.\n
            Il est possible de sélectionner une région à visualiser avec le menu déroulant ci-dessus, ou alors la france entière.\n
            Le liste à côté permet de sélectionner quelle donnée visualiser, par défaut 'pos_7j' représentant le nombre de personnes déclarées positives sur une semaine.\n
            La légende 'Libellé Département' est également interactive et permet d'afficher/cacher les départements de la région sélectionné.

            Sources : https://www.data.gouv.fr/fr/datasets/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/
            
            Notes :
               * On observe qu'il n'y a pas de données avant le 12 Mai 2020. On pourrait supposer que c'est parce que nous ne savions pas testé pour le covid jusque là.
               * On peut notamment voir les deux pics de cas, Octobre-Novembre '2020', amenant au 2nd confinement, et Janvier 2022.
               * Au contraire, on peut observer une baisse net du nombre de cas aux alentours de juillet 2021, correspondant au départ en vacances des français.
            """),
          html.Div([
                    html.Div([ dcc.Graph(id='cvd-slider_graph'), ], style={'width':'90%', }),
                    html.Div([
                        html.Div('Y Axis'),
                        dcc.RadioItems(id='cvd-yaxis-slider', 
                                      options=Y_AXIS_OPTIONS,
                                      value='pos_7j')
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),           
            
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='cvd-year-slider',
                            marks={key : {"label": MONTHS_YEARS[key], "style": {"transform": "rotate(45deg)"}} for key in MONTHS_YEARS},
                            step = 1,
                            value = 0,
                    ),
                    style={'display':'inline-block', 'width':"80%"}
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),
            html.Br(),
            dcc.Markdown("""
            La frise chronologique ci-dessus est interactive, est permet de sélectionner le mois à visualiser.\n
            Notes :
               * Par exemple, on peut observer que le nombre de cas en Auvergne et Rhônes-Alpes est plus beaucoup plus important en décembre, dû aux vacances de skis.
               * Á l'inverse, les régions Occitanie et Provence-Alpes-Côte d'azur sont les deux régions les plus impactés pendant l'été.
               * L'île de France reste la région la plus impactée toute l'année mais on peut observer une baisse des cas lors des périodes de vacances.
            """),
            html.Div([
                    html.Div([ dcc.Graph(id='cvd-2021-graph'), ], style={'width':'90%', }),
                    html.Div([
                        html.Div('Y Axis'),
                        dcc.RadioItems(id='cvd-2021-yaxis', 
                                      options=Y_AXIS_OPTIONS,
                                      value='pos_7j')
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),  
          html.Br(),
            dcc.Markdown("""
            Ce graphique permet de facilement visualiser l'évolution du Covid selon les régions en France pour l'année 2021.
            """),
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

        # self.app.callback(dash.dependencies.Output('cvd-main-graph', 'figure'))(self.update_graph)
        self.app.callback(
                    dash.dependencies.Output('cvd-main-graph', 'figure'),
                    dash.dependencies.Input('cvd-region', 'value'),
                    dash.dependencies.Input('cvd-yaxis', 'value'))(self.update_graph)

        self.app.callback(
                    dash.dependencies.Output('cvd-slider_graph', 'figure'),
                    dash.dependencies.Input('cvd-year-slider', 'value'),
                    dash.dependencies.Input('cvd-yaxis-slider', 'value'))(self.slider_graph)

        self.app.callback(
                    dash.dependencies.Output('cvd-2021-graph', 'figure'),
                    dash.dependencies.Input('cvd-2021-yaxis', 'value'))(self.scatter_graph)

    def scatter_graph(self, yaxis):
      fig = px.line(
          self.regions_2021,
          template='plotly_white',
          x='month',
          y=yaxis,
          color='lib_reg',
          title='Résultats moyens pour 2021'
          #category_orders={'month': ['January','February','March','April','May','June','July','August','September','October','November','December']}
        )
      return fig

    def slider_graph(self, slider, yaxis):
      if slider == None:
        slider = 0

      month_year = MONTHS_YEARS[slider]
      month, year = month_year.split(' ')[1], month_year.split(' ')[0]

      df = self.month_year_df[
        (self.month_year_df.year == int(year)) & 
        (self.month_year_df.month == month)
      ]

      fig = px.bar(
          df,
          template='plotly_white',
          x='lib_reg',
          y=yaxis,
          color='lib_reg',
          title='Résultats par mois'
        )
      fig.update_layout(showlegend=False)
      return fig

    def update_graph(self, region, yaxis):
        if region == 'France':
          regions_df = self.df.reset_index().groupby('date').sum().reset_index()
        else:
          regions_df = self.df[self.df['lib_reg'] == region].reset_index()\

        fig = px.line(
          regions_df,
          template='plotly_white',
          x='date',
          y=yaxis,
          color='lib_dep' if region != 'France' else None,
          title='Toutes les données depuis le début de la pandémie'
        )
        return fig

        
if __name__ == '__main__':
    cvd = CovidBasics()
    cvd.app.run_server(debug=True, port=8051)
