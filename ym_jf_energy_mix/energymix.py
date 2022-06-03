import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

class EnergyMix():

    def make_dataframe(self):
        energymix = 0
        try:
            energymix = pd.read_csv("./data/World_Energy_Consumption.csv", sep=",", skiprows=[], header=0)
        except:
            print('Couldn\'t fin dataset for energymix. Did you run get_data.py ?')
            raise FileNotFoundError
        energymix = energymix.fillna(0.0)
        self.countries = energymix.country.unique()
        energymix = energymix.set_index('country')
        return energymix
    
    def __init__(self, application=None):
        try:
            self.energymix = self.make_dataframe()
        except:
            return
        
        self.productions = self.energymix[['year', 'fossil_electricity', 'hydro_electricity', 'solar_electricity', 'wind_electricity', 'nuclear_electricity']]
        self.productions = self.productions.rename(columns={'fossil_electricity' : 'Fossile', 'hydro_electricity' : 'Hydraulique', 'solar_electricity' : 'Solaire', 'wind_electricity' : 'Eolienne', 'nuclear_electricity' : 'Nucléaire'})
        self.productions = self.productions[self.productions.year >= 1985]
        
        self.coal_use = self.energymix[['iso_code', 'year', 'coal_elec_per_capita']]
        self.coal_use = self.coal_use.rename(columns={'coal_elec_per_capita' : 'KWh de charbon par habitant'})
        self.coal_use = self.coal_use[self.coal_use.year >= 1985]
        self.coal_use = self.coal_use[self.coal_use.iso_code != 0]
        self.coal_use = self.coal_use[self.coal_use.iso_code != 'OWID_WRL']
        
        self.growth = self.energymix[['iso_code', 'year', 'fossil_electricity', 'renewables_electricity', 'nuclear_electricity']]
        self.growth = self.growth[self.growth.iso_code != 0]
        self.growth = self.growth[self.growth.iso_code != 'OWID_WRL']
        self.growth['total_electricity'] = self.growth['fossil_electricity'] + self.growth['renewables_electricity'] + self.growth['nuclear_electricity']
        self.growth['total_change'] = self.growth['total_electricity'][self.growth.year == 2017] - self.growth['total_electricity'][self.growth.year == 1985]
        self.growth['fossil_change'] = self.growth['fossil_electricity'][self.growth.year == 2017] - self.growth['fossil_electricity'][self.growth.year == 1985]
        self.growth['renewables_change'] = self.growth['renewables_electricity'][self.growth.year == 2017] - self.growth['renewables_electricity'][self.growth.year == 1985]
        self.growth = self.growth[self.growth.year == 2017]
        self.growth = self.growth.rename(columns={'total_change': "Variation de la production d'électricité totale en TWh", 'renewables_change': "Variation de la production d'électricité verte en TWh", 'fossil_change': "Variation de la production d'électricité fossile en TWh"})

        self.main_layout = html.Div(children=[
            html.H1(children="Production d'électricité dans le monde : un enjeu climatique"),
            dcc.Markdown("""
                         [La base de donnée](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption) utilisée décrit la production, consommation 
                         électrique de nombreux pays dans le monde en fonction de leur source (charbon, nucléaire, éolien, etc...)  
                         Les enjeux climatiques actuels nécessitent la réduction de la production d'électricité à travers des énergies fossiles 
                         au profit d'énergies renouvelables ou du nucléaire de la part de tous les pays du monde.  
                         La COP21 a fixé un objectif d'une augmentation maximale de la température globale de 2°C d'ici 2100, la plupart des 
                         pays du monde se sont engagés à réduire leur bilan carbone et l'arrêt des centrales à charbon, par exemple, est une façon efficace 
                         d'atteindre cet objectif, cependant certain pays en développement ont des besoins en électricité toujours croissants et 
                         n'ont pas les moyens d'arrêter les énergies fossiles qui ont un coût très bas et une demande technologique faible.
                         
                         A travers cette base de donnée nous allons pouvoir observer les bilans énergetiques des différents pays du monde depuis 
                         1985, voir si le declin du charbon/pétrole est réellement envisageable, observer la réponse des pays en développement malgré 
                         le challenge que la transition leur impose et quels pays ne jouent pas le jeu.
                         
                         Nous avons choisi de commencer les graphes à partir de 1985 car de nombreuses catégories étaient trop incomplètes avant cette 
                         date pour produire quelquechose ayant un sens.
                         
                         La base de donnée différencie consommation et production, du au fait que certains pays vendent leurs électricité, nous utiliserons la 
                         production pour nos graphes.
                        """),
            html.H3(children='Mix énergétique des différents pays du monde'),
            html.Div([
                html.Div([ html.Div('Pays / Zone géographique', style={'width': '8em', 'display': 'inline-block'}),
                           dcc.Dropdown(
                               id='graph1_countries',
                               options=self.countries,
                               value='France',
                               searchable=True,
                               clearable=False,
                               style={'width': '22em', 'display': 'inline-block'}
                           )
                         ], style={'width': '30em'} )
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
            }),
            html.Div([ dcc.Graph(id='graph1'), ], style={'width':'100%', }),
            dcc.Markdown("""
                          On constate que beaucoup de pays sont encore très dépendants aux énergies fossile pour leur production électrique.  
                          Les pays avec un grosse croissance en production sont d'autant plus dépendants car ils doivent l'améliorer 
                          rapidement et une il est plus facile de construire une centrale à charbon qu'un parc éolien.
                          """),
            html.Br(),
            html.H3(children="Production électrique au charbon dans le monde"),
            html.Div([dcc.Graph(id='graph2'), ], style={'width': '100%'}),
            html.Div([
                html.Div([html.Div('Année', style={'width': '4em', 'display': 'inline-block'}),
                            dcc.Dropdown(
                                id='graph2_year',
                                options=[i for i in range(1985, 2019)],
                                value=2017,
                                clearable=False, 
                                searchable=True,
                                style={'width': '12em', 'diplay': 'inline-block'}
                            )], 
                            style={'width': '16em', 'display': 'flex'}
                            ),
            ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'flex-start',
                    }),
            dcc.Markdown("""
                          Comme dit précédemment, on observe que parmi les plus gros consommateurs de charbon se trouvent les 
                          pays en développement rapide comme la Chine, l'Inde et le Brésil.  
                          On notera aussi la présence des Etats-Unis et particulièrement l'Australie dans les plus gros 
                          producteurs. Ces 2 pays ont de grosses ressources en charbon ce qui explique ces données mais ont 
                          également signés les accords de Paris.  
                          Est ce que leur production diminue ou ne respectent-ils pas ces accords?
                          """),
            html.Br(),
            html.Div([dcc.Graph(id='graph3'), ], style={'width': '100%'}),
            html.Div([
                html.Div([html.Div('Type de source', style={'width': '8em', 'display': 'inline-block'}),
                            dcc.RadioItems(
                               id='graph3_source',
                               options=[{'label':'Totale', 'value':0}, 
                                        {'label':'Renouvelable','value':1},
                                        {'label':'Fossile','value':2}],
                               value=0,
                               labelStyle={'display':'block'},
                           )], 
                            style={'width': '30em', 'display': 'flex'}
                            ),
            ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'flex-start',
                    }),
            dcc.Markdown("""
                          Ce graphe confirme les spéculations à propos des pays en développement, on notera qu'on observe 
                          une faible croissance de la production à partir d'énergies fossiles en Australie ce qui indique 
                          que cette production a stagnée et que des efforts sont faits.
                          """),
            html.Br(),
            html.Br(),
            dcc.Markdown("""
                        #### À propos
                        * [Source de la base de donnée](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption)
                        * Auteurs : Yorick Madelain, Jordan Failloux
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
            
        self.app.callback(
                    dash.dependencies.Output('graph1', 'figure'),
                    [ dash.dependencies.Input('graph1_countries', 'value')])(self.update_graph1)
        self.app.callback(
                    dash.dependencies.Output('graph2', 'figure'),
                    [ dash.dependencies.Input('graph2_year', 'value')])(self.update_graph2)
        
        self.app.callback(
                    dash.dependencies.Output('graph3', 'figure'),
                    [ dash.dependencies.Input('graph3_source', 'value')])(self.update_graph3)
        
    def update_graph1(self, country):
        fig = px.area(self.productions.loc[country], 'year', ['Fossile', 'Hydraulique', 'Solaire', 'Eolienne', 'Nucléaire'],
            title = None,
                labels ={
                    "year": "Année",
                    "value": "Quantité d'électricité générée en TWh",
                    "variable": "Type de source"
                })
        return fig
    
    def update_graph2(self, year):
        fig = px.choropleth(self.coal_use[self.coal_use.year == year], locations='iso_code', color='KWh de charbon par habitant', color_continuous_scale=px.colors.sequential.turbid,
            title = None,
                labels ={
                })
        return fig
    
    def update_graph3(self, energy_type):
        if energy_type == 0:
            fig = px.choropleth(self.growth, locations='iso_code', color="Variation de la production d'électricité totale en TWh", color_continuous_scale=px.colors.sequential.thermal,
                                title = "Variation des productions d'électricité entre 1985 et 2017")
            return fig
        if energy_type == 1:
            fig = px.choropleth(self.growth, locations='iso_code', color="Variation de la production d'électricité verte en TWh", color_continuous_scale=px.colors.sequential.thermal,
                                title = "Variation des productions d'électricité entre 1985 et 2017")
            return fig
        if energy_type == 2:
            fig = px.choropleth(self.growth, locations='iso_code', color="Variation de la production d'électricité fossile en TWh", color_continuous_scale=px.colors.sequential.thermal,
                                title = "Variation des productions d'électricité entre 1985 et 2017")
            return fig
        
if __name__ == '__main__':
    nrg = EnergyMix()
    nrg.app.run_server(debug=True, port=8051)