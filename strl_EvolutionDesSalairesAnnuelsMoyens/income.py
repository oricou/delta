import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
import json

class Income():
    
    def __init__(self, application = None):
        if application == None:
            self.root = ""
        else:
            self.root = "./strl_EvolutionDesSalairesAnnuelsMoyens/"
        self.hf = pd.read_pickle(self.root + "data/hf.pkl")
        self.hf_melted = pd.read_pickle(self.root + "data/hf_melted.pkl")
        self.pib_idh_salary = pd.read_pickle(self.root + "data/pib_idh_salary.pkl")
        self.salary = pd.read_pickle(self.root + "data/salary.pkl")
        # Carte de l'Europe
        self.map_europe = json.load(open(self.root + 'data/custom.geo.json')) # on charge qu'on a généré de l'europe 
        
#Region HTML
        self.main_layout = html.Div(children=[
        html.H1(children='Évolution des salaires dans le monde'),

        html.Div([
                dcc.Graph(id='salary-graph'),
            
        dcc.Checklist(
                            id='SalairePays',
                            options=[{'label': i, 'value': i} for i in sorted(self.salary.index.unique())],
                            value=["France", "États-Unis", "Japon", "Italie", "Belgique"],
                            labelStyle={'border': '1px transparent solid', 'display':'inline-block', 'width':'12em',},
                        ),
        html.Br(),    
        dcc.Markdown("Le salaire moyen dans les pays connait une croissance assez constante en période stable au fur et à mesure du temps."),
        dcc.Markdown("Cependant la tendance de la courbe est très influencée par les évènements qui touche la population."),
        dcc.Markdown("Durant la période du COVID19:"),
        dcc.Markdown("- On remarque qu'il y a une baisse du salaire à la fin de 2019 pour certains pays d'Europe comme la France, l'Italie ou la Belgique dû au confinement."),
        dcc.Markdown("- Les autres pays qui n'ont pas adopté le confinement eux ne voit pas de baisse comme on peut le voir pour les Etats unis fin 2019/ début 2020."),
        dcc.Markdown("Un des facteurs qui pourrait expliquer cette croissance (hormis période Covid) en France est que le salaire minimum augmente au fil des années. De même pour l'Allemagne."),
        ], ),
        
        html.Div([ dcc.Markdown('''
        ## Le PIB et le salaire influe-t'il sur l'IDH?
        '''),
            dcc.Graph(id="pib-idh-salary-graph", figure = self.create_anim_graph())]),
            
        dcc.Markdown("La tendance générale est que la PIB augmente avec le temps mais que l'IDH n'augmente pas forcément"),
        dcc.Markdown("Mais tout de même, pour la majorité des cas un haut PIB signifie un haut IDH et vice-versa:"),
        dcc.Markdown("- On peut observer le Mexique qui à un des plus petits salaire moyen, PIB et a donc un IDH bas."),
        dcc.Markdown("- Alors que les Etats-Unis restent sur le haut du tableau."),
        dcc.Markdown("Mais il existe tout de même des exceptions à cette règle notamment:"),
        dcc.Markdown("- La Norvège qui même si n'a pas le plus haut salaire moyen et PIB reste un des plus gros IDH grâce aux régions pétrolifères."),
        
            
                
        html.Div([dcc.Markdown('''
        ## Inegalité des salaires Homme Femme en Europe
        '''), 
                  dcc.Markdown("Cette map est interactive, pour afficher les données d'un pays, il suffit de cliquer dessus sur la carte."),
                  dcc.Graph(id="Salary-hf"),
                 html.Div([dcc.Dropdown([str(i) for i in range(2010,2021)], '2010', id='hf-date-dropdown', style={"width":"25%"},searchable=False,clearable=False)
]),
                  
                  html.Div([
                  dcc.Graph(id="Salary-hf-bar", style={"width":"50%"}),
                  html.Div([
                      dcc.Markdown("""On peut observer qu'il existe une inégalité des salaires hommes et femmes en Europe mais selon les pays la différence est variable :"""),
                      dcc.Markdown('    - En France, la différence à tendance à augmenter avec un pic en 2018 qui est récent.'),
                      dcc.Markdown("    - En Lettonie, l'écart croit de manière constante."),
                      dcc.Markdown("    - Cependant certain pays font des efforts comme l'Estonie et voit une baisse constante de l'inégalité."),
                      dcc.Markdown("La tendance générale est que la différence en pourcentage des salaires décroit en Europe."),
                  ], style={"width":"50%", 'padding-top':'100px'}),                                                                       
                 ], style={"display": 'flex', 'height': '500px'}),
                  ]),
            html.Div([dcc.Markdown('''
            ## A Propos
            ### Auteurs:
            - Richard LAY richard.lay
            - Steven TIEN steven.tien
            ### Sources:
            - PIB : https://data.oecd.org/gdp/gross-domestic-product-gdp.htm
            - IDH : https://hdr.undp.org/en/indicators/137506#
            - PaysIso : https://gist.github.com/radcliff/f09c0f88344a7fcef373
            - Salaire Moyen dans le monde : https://stats.oecd.org/viewhtml.aspx?datasetcode=AV_AN_WAGE&lang=fr
            - Inégalité homme/femme : https://ec.europa.eu/eurostat/databrowser/view/SDG_05_20/default/table?lang=en
            ''')
            ]),
        ],
         style={'margin':'50px'})
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
#Region callback   
        self.app.callback(
            dash.dependencies.Output('salary-graph', 'figure'),
            [dash.dependencies.Input('SalairePays', 'value')])(self.create_graph_stv)
        
        self.app.callback(
            dash.dependencies.Output('Salary-hf', 'figure'),
            [dash.dependencies.Input('hf-date-dropdown', 'value')])(self.create_map_hf)
        
        self.app.callback(
            dash.dependencies.Output('Salary-hf-bar', 'figure'),
            dash.dependencies.Input('Salary-hf', 'clickData'))(self.get_country)
        
        
#Region créateur de graphes.    
    def create_graph_stv(self, x, titre="Évolution des salaires"):
        fig = px.line(title=titre, )
        for el in x:
            fig.add_scatter(x=self.salary[self.salary.index == el]['TIME'], y=self.salary[self.salary.index == el]['Value'], name = el)
        fig.update_layout(yaxis = dict( title = 'Salaire en USD'), xaxis = dict( title = 'Temps en année'))
        return fig
    
    def create_anim_graph(self):
        fig = px.scatter(self.pib_idh_salary.sort_values(by=['TIME', 'idh']), x='pib', y='idh', color="Pays", hover_name='Pays',
                 title="Relation entre IDH et PIB entre 2000 et 2020",
                 size='salary', size_max = 50,
                 animation_frame='TIME', animation_group="Pays", range_x=[0,150000],
                 height=700)
        fig.update_layout(yaxis = dict( title = 'IDH'), xaxis = dict( title = 'PIB'))
        return fig
    
    def create_map_hf(self, date):
        fig = px.choropleth_mapbox(self.hf, geojson=self.map_europe, locations='Country', color=str(date) + ' ', featureidkey = 'properties.name_long',
                            color_continuous_scale="Bluered",
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": 55, "lon": 2},
                            opacity=0.5,
                            labels={date+' ' :'Écart de salaire en %'},
                            title="Écart de salaire entre les hommes et les femmes")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    def create_hf_bar_plot(self, pays):
        fig = px.bar(self.hf_melted[self.hf_melted["Country"] == pays], x=[str(i) + ' ' for i in range(2010,2021)], y ='ecart', log_y=True, title=pays)
        fig.update_layout(yaxis = dict( title = 'Écart des salaires en %'), xaxis = dict( title = 'Année'))
        return fig
    
    def get_country_data(self, clickData):
        if clickData == None:
            return self.create_hf_bar_plot("France")
        else:
            return self.create_hf_bar_plot(clickData["points"][0]["location"])
    
    def get_country(self, clickData):
        return self.get_country_data(clickData)
    
    
if __name__ == '__main__':
    inc = Income()
    inc.app.run_server(debug=True, port=8051)