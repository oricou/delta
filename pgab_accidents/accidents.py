import glob
import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import calendar as cal

class Accidents:
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = pd.concat([pd.read_pickle(f) for f in glob.glob('data/acc_caracs_grav-*')]).sort_values(['year', 'grav'],
               ascending = [True, False])
        self.df.rename(columns = {'grav':'Gravité', 'year':'Année', 'mois':'Mois'}, inplace = True)
        bar_fig = px.histogram(self.df, x="Année", color="Gravité")
        self.zoom=4
        self.center=dict(lat=46.7111, lon=1.7191)
        
        pio.templates["missing"] = go.layout.Template(
            layout_annotations=[
                dict(
                    name="missing data watermark",
                    text="MISSING DATA",
                    textangle=-20,
                    opacity=.4,
                    font=dict(color="black", size=100),
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                )
            ]
        )

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des accidents de la route en France métropolitaine entre 2005 et 2020'),
            html.Div([
                html.Div([ dcc.Graph(id='pgab-acc-main-graph'), ], style={'width':'100%', }),
                html.Div([ dcc.RadioItems(id='pgab-acc-type', 
                                         options=[{'label':'Heatmap', 'value':0},
                                                  {'label':'Emplacements exacts', 'value':1}], 
                                         value=0,
                                         labelStyle={'display':'block'}),
                           html.Div(html.Button(self.START, id='pgab-button-start-stop', style={'display':'inline-block'}), style={'margin-right':'15px', 'width': '7em', 'float':'right'}),
                         ]),
                     ]),
            html.Div([
                html.Br(),
                html.Div(
                    dcc.Slider(
                            id='pgab-year-slider',
                            min=2005,
                            max=2020,
                            step = 1,
                            value=2005,
                            marks={str(year): str(year) for year in range(2005, 2021)},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(
                    id='pgab-auto-stepper',
                    interval=1500,
                    max_intervals = -1,
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),
            html.Div([ dcc.Graph(id='pgab-acc-month-bar-graph'), ], style={'width':'100%', }),
            dcc.Markdown("""
            Carte interactive des accidents de la route recensés entre 2005 et 2020.
            
            Utilisez le slider afin de sélectionner l'année.
            
            L'année 2009 reste manquante (fichier invalide), et avant 2015 la plupart des régions ne donnent pas de coordonnées GPS, les données mises à disposition sont incomplètes.
            
            La carte comporte plusieurs calques:
            * **Heatmap** des accidents
            * **Emplacements exacts** des accidents
            
            __Information complémentaire__, la gravité d'un accident correspond à:
            * **1** | Indemne
            * **2** | Blessures légères
            * **3** | Blessures graves
            * **4** | Blessures mortelles
            """, style={'margin-top': '3rem'}),
            
            html.Div([ dcc.Graph(id='acc-bar-graph', figure=bar_fig), ], style={'width':'100%', }),
            dcc.Markdown("""
            Histogramme des accidents de la route recensés entre 2005 et 2020.
            
            L'année 2009 reste manquante, les données mises à disposition sont incomplètes.

            #### À propos
            * Données: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/)

            &copy; 2022 Paul Galand & Ancelin Bouchet
            """, style={'margin-top': '3rem'}),
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
            'display': 'flex',
            'flex-direction': 'column'
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('pgab-acc-month-bar-graph', 'figure'),
            dash.dependencies.Input('pgab-year-slider', 'value'))(self.update_month_bar_graph)
        self.app.callback(
            dash.dependencies.Output('pgab-acc-main-graph', 'figure'),
            [ dash.dependencies.Input('pgab-acc-type', 'value'),
              dash.dependencies.Input('pgab-year-slider', 'value')])(self.update_main_graph)
        self.app.callback(
            dash.dependencies.Output('pgab-button-start-stop', 'children'),
            dash.dependencies.Input('pgab-button-start-stop', 'n_clicks'),
            dash.dependencies.State('pgab-button-start-stop', 'children'))(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output('pgab-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('pgab-button-start-stop', 'children')])(self.run_movie)
        self.app.callback(
            dash.dependencies.Output('pgab-year-slider', 'value'),
            dash.dependencies.Input('pgab-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('pgab-year-slider', 'value'),
             dash.dependencies.State('pgab-button-start-stop', 'children')])(self.on_interval)

    def update_month_bar_graph(self, year):
        dfg = self.df
        dfg = dfg[dfg['Année'] == str(year)]
        if dfg.empty:
            pio.templates.default = "missing"
        else:
            pio.templates.default = None
        return px.histogram(dfg, x="Mois", color="Gravité")

    def update_main_graph(self, acc_type, year):
        dfg = self.df
        dfg = dfg[dfg['Année'] == str(year)]
        if dfg.empty:
            pio.templates.default = "missing"
        else:
            pio.templates.default = None
        if acc_type:
            fig=px.scatter_mapbox(dfg, lat='lat', lon='long',
                                  color='Gravité', mapbox_style='carto-positron',
                                  zoom=self.zoom, center=self.center,
                                  color_continuous_scale=px.colors.sequential.Bluered,
                                  custom_data=['jour', 'Mois', 'Année', 'Gravité'])
            fig.update_layout(height=800)
        else:
            fig=px.density_mapbox(dfg, z=None, lat='lat', lon='long',
                                  radius=5, opacity=.6, mapbox_style='carto-positron',
                                  zoom=self.zoom, center=self.center,
                                  color_continuous_scale=px.colors.diverging.Picnic,
                                  custom_data=['jour', 'Mois', 'Année', 'Gravité'])
            fig.update_layout(coloraxis_showscale=False, height=800)
        fig.update_traces(hovertemplate="Date: %{customdata[0]}/%{customdata[1]}/%{customdata[2]} | Gravité: %{customdata[3]}")
        fig.update_layout(uirevision='constant')
        return fig
    
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    def run_movie(self, text):
        if text == self.START:
            return 0 
        else:
            return -1
        
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:
            if year == 2020:
                return 2005
            if year == 2008:
                return 2010
            return year + 1
        return year
        
    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    acc = Accidents()
    acc.run(port=8065)
