import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
import json
"""
Ce fichier python ne peut pas être utilisé par elle même car les path vers les data set on été mis pour pouvoir fonctionner avec le delta.py
"""
class Income():
    
    def __init__(self, application = None):
#Region nettoyage des données.
        # Salaire
        #self.salary = pd.read_csv("./esam_EvolutionDesSalairesAnnuelsMoyens/data/AV_AN_WAGE_15032022112411307.csv")
        #self.salary = self.salary[self.salary["SERIES"] == "USDPPP"] # On garde seulement les lignes au prix USD
        #self.salary = self.salary.drop(columns=["Flag Codes", "Flags", "PowerCode", "PowerCode Code", "Reference Period Code", "Temps"]) 
        #
        #self.salary = self.salary.set_index("Pays")
        #self.salary_france = self.salary[self.salary.index == "France"]
        #
        ## PIB
        #self.pib = pd.read_csv("./esam_EvolutionDesSalairesAnnuelsMoyens/data/DP_LIVE_24032022132056468.csv")  # Value en millions
        #self.pib = self.pib.drop(columns=["Flag Codes"])
        #self.pib = self.pib.rename(columns={'LOCATION' : 'COUNTRY'})
        #
        ## Merge salary et pib
        #self.pib_salary = self.salary.reset_index().merge(self.pib, how='inner', on=['COUNTRY', 'TIME']).set_index('Pays')
        #self.pib_salary = self.pib_salary.rename(columns={'Value_y' : "pib", 'Value_x' : "salary"})
        
        # IDH
        #self.idh = pd.read_csv("./esam_EvolutionDesSalairesAnnuelsMoyens/data/Human Development Index (HDI).csv", sep =',', encoding='latin-1', skiprows=4, header = 1)
        #self.idh = self.idh.loc[:, ~self.idh.columns.str.contains('^Unnamed')]
        #self.idh = self.idh.drop(columns=["HDI Rank"])
        #self.idh.columns = self.idh.columns.astype(str)
        #self.idh = self.idh.loc[:, ~self.idh.columns.str.contains('^1')] #On garde seulement les colonnes des années 2000+
        #self.idh = self.idh.drop(self.idh.tail(18).index)#remove les dernieres rows qui ne nous servent pas
        #self.idh['Country'] = self.idh['Country'].astype(str)
        #self.idh['Country'] = self.idh['Country'].apply(lambda x: x[1:]) # Remove le premier char invisible.
        #self.idh = self.idh.melt(id_vars=["Country"], var_name="Date", value_name="idh").sort_values(by = ["Country", "Date"]).reset_index(drop=True) #Avant: colonnes = dates et mtn: on les transforme en lignes.

        # Pays iso
        #self.pays_iso = pd.read_csv("./esam_EvolutionDesSalairesAnnuelsMoyens/data/wikipedia-iso-country-codes.csv", sep =',')
        #self.pays_iso = self.pays_iso.drop(columns=['ISO 3166-2', 'Numeric code'])
        #self.pays_iso = self.pays_iso.rename(columns={"English short name lower case": "Country"})
        #self.pays_iso['Country'] = self.pays_iso['Country'].astype(str)
        #
        #self.idh_iso = pd.merge(self.pays_iso, self.idh, on=['Country'])
        #self.idh_iso = self.idh_iso.rename(columns = {"Alpha-3 code" : "COUNTRY", "Date" : "TIME"})
        #self.idh_iso["TIME"] = self.idh_iso["TIME"].astype(int)  # Convert le type de TIME en int pour pouvoir le merge plus tard 
#
        ## Merge idh et pib_salary
        #self.pib_idh_salary = self.pib_salary.reset_index().merge(self.idh_iso, how='inner', on=['COUNTRY', 'TIME']).set_index('Pays') #Pour avoir le nom des pays complet et faire le lien avec les autres dataframes
        #self.pib_idh_salary["Pays"] = self.pib_idh_salary.index 
        
        # Salaire homme/femme
        #self.hf = pd.read_csv("./esam_EvolutionDesSalairesAnnuelsMoyens/data/sdg_05_20_tabular-1.tsv", sep='\t', na_values=": ")
        #self.hf = self.hf.drop(columns=['2002 ', '2006 ', '2007 ', '2008 ', '2009 '])
        #self.hf['freq,unit,nace_r2,geo\TIME_PERIOD'] = self.hf['freq,unit,nace_r2,geo\TIME_PERIOD'].astype(str)
        #self.hf['freq,unit,nace_r2,geo\TIME_PERIOD'] = self.hf['freq,unit,nace_r2,geo\TIME_PERIOD'].apply(lambda x: x.split(',')[-1])
        #self.hf = self.hf.rename(columns = {"freq,unit,nace_r2,geo\TIME_PERIOD":"Pays"})
        #self.hf = self.hf.set_index("Pays")
        #self.hf = self.hf.apply(lambda x : x.astype(str))
        #self.hf = self.hf.apply(lambda x : x.apply(lambda y: y.split()[0]))
        #self.hf = self.hf.apply(lambda x : x.astype(float))
        #self.hf = self.hf.loc[self.hf.count(1) > self.hf.shape[1]/2, self.hf.count(0) > self.hf.shape[0]/2] #on supprime les             lignes qui on plus de 50% de valeurs manquantes.
        #self.hf = self.hf.drop(index=['EU28', 'EU27_2020', 'EA19']) #inintéressant
        #self.hf = self.hf.fillna(method="ffill", axis=1)
        #self.hf["Alpha-2 code"] = self.hf.index
        #self.hf.loc["UK", "Alpha-2 code"] = "GB" #L'angleterre = GB en alpha code 2
        #
        ## Merge hf et pays iso
        #self.hf = pd.merge(self.hf, self.pays_iso, how='inner', on="Alpha-2 code")
        #self.hf_melted = self.hf.melt(id_vars=["Country", "Alpha-2 code", "Alpha-3 code"], var_name="Date", value_name="ecart").sort_values(by = ["Country", "Date"]).reset_index(drop=True)# on met les date en ligne et plus en colonnes.
        
        self.hf = pd.read_pickle("./strl_EvolutionDesSalairesAnnuelsMoyens/data/hf.pkl")
        self.hf_melted = pd.read_pickle("./strl_EvolutionDesSalairesAnnuelsMoyens/data/hf_melted.pkl")
        self.pib_idh_salary = pd.read_pickle("./strl_EvolutionDesSalairesAnnuelsMoyens/data/pib_idh_salary.pkl")
        self.salary = pd.read_pickle("./strl_EvolutionDesSalairesAnnuelsMoyens/data/salary.pkl")
        # Carte de l'Europe
        self.map_europe = json.load(open('./strl_EvolutionDesSalairesAnnuelsMoyens/data/custom.geo.json')) # on charge qu'on a généré de l'europe 
        
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
    
    
#if __name__ == '__main__':
#    inc = Income()
#    inc.app.run_server(debug=True, port=8051)