import os
import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

from ljad_prenoms.get_data import * 

def compute_percentage(df, groupby_level, col):
    return 100 * df[col] / df.groupby(level=groupby_level)[col].sum()

def group_val_by_idx_lvl(srt_df, reindex, lvl):
    return {name: group['percentage'].rename(name).droplevel(lvl).reindex(reindex, fill_value=0) for name, group in srt_df.groupby(level=lvl)}

def group_val_by_idx_lvl_gdr(srt_df_gdr, gdr, reindex, lvl):
    srt_df = srt_df_gdr.loc[(gdr, slice(None), slice(None), slice(None))]
    return group_val_by_idx_lvl(srt_df, reindex, lvl)

def get_corr_dpt_cat_name(all_cat_dict, all_prn_dict, dpt, cat, name):
    cat_dpt = all_cat_dict[cat].loc[dpt]
    prn_dpt = all_prn_dict[name].loc[dpt]
    
    return pd.DataFrame(data=[cat_dpt, prn_dpt]).T.corr().loc[cat, name]

def get_corr_all_dpt_cat_name(all_cat_dict, all_prn_dict, cat, name):
    # Pour chaque département de la métropole
    return {i: get_corr_dpt_cat_name(all_cat_dict, all_prn_dict, i, cat, name) for i in range(1, 96)}

DEPARTMENTS = {
    1: 'Ain', 
    2: 'Aisne', 
    3: 'Allier', 
    4: 'Alpes-de-Haute-Provence', 
    5: 'Hautes-Alpes',
    6: 'Alpes-Maritimes', 
    7: 'Ardèche', 
    8: 'Ardennes', 
    9: 'Ariège', 
    10: 'Aube', 
    11: 'Aude',
    12: 'Aveyron', 
    13: 'Bouches-du-Rhône', 
    14: 'Calvados', 
    15: 'Cantal', 
    16: 'Charente',
    17: 'Charente-Maritime', 
    18: 'Cher', 
    19: 'Corrèze', 
    20: 'Corse', 
    21: 'Côte-d\'Or', 
    22: 'Côtes-d\'Armor', 
    23: 'Creuse', 
    24: 'Dordogne', 
    25: 'Doubs', 
    26: 'Drôme',
    27: 'Eure', 
    28: 'Eure-et-Loir', 
    29: 'Finistère', 
    30: 'Gard', 
    31: 'Haute-Garonne', 
    32: 'Gers',
    33: 'Gironde', 
    34: 'Hérault', 
    35: 'Ille-et-Vilaine', 
    36: 'Indre', 
    37: 'Indre-et-Loire',
    38: 'Isère', 
    39: 'Jura', 
    40: 'Landes', 
    41: 'Loir-et-Cher', 
    42: 'Loire', 
    43: 'Haute-Loire',
    44: 'Loire-Atlantique', 
    45: 'Loiret', 
    46: 'Lot', 
    47: 'Lot-et-Garonne', 
    48: 'Lozère',
    49: 'Maine-et-Loire', 
    50: 'Manche', 
    51: 'Marne', 
    52: 'Haute-Marne', 
    53: 'Mayenne',
    54: 'Meurthe-et-Moselle', 
    55: 'Meuse', 
    56: 'Morbihan', 
    57: 'Moselle', 
    58: 'Nièvre', 
    59: 'Nord',
    60: 'Oise', 
    61: 'Orne', 
    62: 'Pas-de-Calais', 
    63: 'Puy-de-Dôme', 
    64: 'Pyrénées-Atlantiques',
    65: 'Hautes-Pyrénées', 
    66: 'Pyrénées-Orientales', 
    67: 'Bas-Rhin', 
    68: 'Haut-Rhin', 
    69: 'Rhône',
    70: 'Haute-Saône', 
    71: 'Saône-et-Loire', 
    72: 'Sarthe', 
    73: 'Savoie', 
    74: 'Haute-Savoie',
    75: 'Paris', 
    76: 'Seine-Maritime', 
    77: 'Seine-et-Marne', 
    78: 'Yvelines', 
    79: 'Deux-Sèvres',
    80: 'Somme', 
    81: 'Tarn', 
    82: 'Tarn-et-Garonne', 
    83: 'Var', 
    84: 'Vaucluse', 
    85: 'Vendée',
    86: 'Vienne', 
    87: 'Haute-Vienne', 
    88: 'Vosges', 
    89: 'Yonne', 
    90: 'Territoire de Belfort',
    91: 'Essonne', 
    92: 'Hauts-de-Seine', 
    93: 'Seine-Saint-Denis', 
    94: 'Val-de-Marne', 
    95: 'Val-d\'Oise',
}

class Prenoms():
    xls = pd.ExcelFile('ljad_prenoms/data/irsoceds2013_T102.xls')

    def __init__(self, application=None):
        self.dpt = list(range(1, 96))

        if os.path.exists("ljad_prenoms/data/prenoms.pkl.gz"):
            self.prenoms = pd.read_pickle("ljad_prenoms/data/prenoms.pkl.gz")
        else:
            self.prenoms = get_prenoms().set_index(['sexe', 'dpt', 'annais', 'preusuel'])
            self.prenoms.sort_index(inplace=True)
            self.prenoms['percentage'] = compute_percentage(self.prenoms, [0, 1, 2], 'nombre')
            self.prenoms.index = self.prenoms.index.set_levels(self.prenoms.index.levels[1].astype(int), level=1)
            self.prenoms.to_pickle("ljad_prenoms/data/prenoms.pkl.gz")

        # Metropole uniquement
        sorted_prenoms = self.prenoms.loc[(slice(96),),:].sort_values('nombre', ascending=False).sort_index()

        self.secteurs = {
            secteur[4:] : pd.read_excel(Prenoms.xls, secteur).iloc[1,0].split('-')[1]
            if len(secteur) > 6
            else pd.read_excel(Prenoms.xls, secteur).iloc[1,0][7:]
            for secteur in Prenoms.xls.sheet_names[:48]
        }
        self.all_job_sectors = read_all_sheet_emploi(Prenoms.xls)

        self.unique_categories = []
        for cat in self.secteurs.keys():
            if all(oth == cat or (not oth.startswith(cat)) for oth in self.secteurs.keys()):
                self.unique_categories.append(cat)

        if os.path.exists("ljad_prenoms/data/all_cat_dict_mixed.pkl.gz"):
            self.all_cat_dict_mixed = pd.read_pickle("ljad_prenoms/data/all_cat_dict_mixed.pkl.gz")
            cat_index = self.all_cat_dict_mixed.index
        else:
            base_cat_all_emplois_gdr = self.all_job_sectors.loc[(slice(None), slice(None), slice(None), self.unique_categories), :].copy()
            base_cat_all_emplois_gdr['percentage'] = compute_percentage(base_cat_all_emplois_gdr, [0, 1, 2], 'nombre')
            base_cat_all_emplois_gdr = base_cat_all_emplois_gdr.sort_values('nombre', ascending=False).sort_index(level=[0,1,2])
            mixed_all_cat = base_cat_all_emplois_gdr.groupby(level=['dpt', 'annee', 'categorie']).sum()
            mixed_all_cat['percentage'] = compute_percentage(mixed_all_cat, [0, 1], 'nombre')
            cat_index = base_cat_all_emplois_gdr.index.droplevel(['categorie', 'sexe']).unique()
            self.all_cat_dict_mixed = pd.DataFrame.from_dict(group_val_by_idx_lvl(mixed_all_cat, cat_index, 'categorie'))
            self.all_cat_dict_mixed.to_pickle("ljad_prenoms/data/all_cat_dict_mixed.pkl.gz")

        if os.path.exists("ljad_prenoms/data/all_prn_dict_mixed.pkl.gz"):
            self.all_prn_dict_mixed = pd.read_pickle("ljad_prenoms/data/all_prn_dict_mixed.pkl.gz")
        else:
            mixed_all_prn = sorted_prenoms.groupby(level=['dpt', 'annais', 'preusuel']).sum()
            mixed_all_prn['percentage'] = compute_percentage(mixed_all_prn, [0, 1], 'nombre')
            self.all_prn_dict_mixed = pd.DataFrame.from_dict(group_val_by_idx_lvl(mixed_all_prn, cat_index, 'preusuel'))
            self.all_prn_dict_mixed.to_pickle("ljad_prenoms/data/all_prn_dict_mixed.pkl.gz")

        # self.population = get_populations()
        self.departements = get_france_geojson()
        self.chomage = get_chomage()
        
        # self.unique_prenoms = self.prenoms.preusuel.unique()
        self.unique_prenoms = sorted_prenoms.groupby(level=3).sum().sort_values('nombre', ascending=False).index

        self.years = np.arange(1994, 2013)

        
        self.main_layout = html.Div(children=[
            html.H3(children='Historique des prénoms de naissance, secteur d\'activité et chomâge par département'),
            html.Div([
                         html.Div([ dcc.Graph(id='map', style={'height': '40em'}), ],
                                  style={'height':'100%','width':'54%', 'display': 'inline-block'}),
                         html.Div([ dcc.Graph(id='graph', style={'height': '40em'}), ],
                                  style={'height': '100%','width':'46%', 'display': 'inline-block'}),
                     ],style={
                        'backgroundColor': 'gray',
                        'display':'flex',
                        'flexDirection':'row',
                        'justifyContent':'flex-start',
                        'width': '100%',
                     }),
            html.Br(),
            html.Div([
                html.Div([ html.Div('Type de cartes'),
                           dcc.RadioItems(
                               id='map-type',
                               options=[{'label':'Occurrence des prénoms de naissance', 'value':0}, 
                                        {'label':'Taux de Chomage','value':1},
                                        {'label':'Secteur d\'activité','value':2},
                                        {'label':'Corrélation Occurrence prénom de naissance / Secteur d\'activité','value':3}],
                               value=0,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em'} ),
                html.Div([ html.Div('Prénom de naissance', id='prenom'),
                            dcc.Dropdown(
                                 id='name',
                                 options=[{'label': i, 'value': i} for i in self.unique_prenoms],
                                 value='guillaume'
                             ), ], style={'width':'9em'}),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Département', id='departements'),
                            dcc.Dropdown(
                                 id='dpt',
                                 options=[{'label': f"{i} - {DEPARTMENTS[i]}", 'value': i} for i in self.dpt],
                                 value=None
                             ), ], style={'width':'9em'}),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Année ref.'),
                           dcc.Dropdown(
                               id='year',
                               options=[{'label': i, 'value': i} for i in self.years],
                               value=2000,
                           ),
                         ], style={'width': '9em'} ),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Sexe', id='gender'),
                           dcc.RadioItems(
                               id='sexe',
                               options=[{'label':'Tous', 'value':0}, 
                                        {'label':'Homme','value':1},
                                        {'label':'Femme','value':2}],
                               value=0,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div("Secteur d'activité", id='sheet'),
                           dcc.Dropdown(
                               id='secteurs',
                               options=[{'label': description, 'value': code}
                                     for code, description in self.secteurs.items()],
                               value='TAZ', # première feuille, 'Tous secteurs'
                               optionHeight=60,
                           ),
                         ], style={'width': '35em'} ), # bas D haut G
                html.Div(style={'width':'2em'}),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Hr(),
                dcc.Markdown("""
                La carte est intéractive. En passant la souris sur  les départements vous avez une infobulle.

                Notes :
                   * Les départements de la petite et de la grande couronne de Paris et de Paris même
                   (75,77,78,91,92,93,94,95) sont apparuts en 1968 suite à la
                   [réorganisation de la région parisienne de 1964](https://fr.wikipedia.org/wiki/R%C3%A9organisation_de_la_r%C3%A9gion_parisienne_en_1964).
                   * Les données des noms de traitent pas les deux départements de la Corse séparemment.
                   * Les données du chômage et de l'emploi ne traitent pas les territoires d'Outre-mer.
                   * De fait, les données ne traiteront que les données de métropole, la Corse ne constituera qu'un seul département.
                   * Sources : 
                      * [Historique des prénoms donnés à la naissance, par département](https://www.insee.fr/fr/statistiques/2540004#consulter) - Etat Civil - INSEE
                      * [Historique des populations communales](https://www.insee.fr/fr/statistiques/3698339) - Recensement de la population de 1876 à 2019 - INSEE
                      * [Chômage départemental](https://www.insee.fr/fr/statistiques/1409932?sommaire=1409948) de 1982 à 2014 - INSEE
                      * [Emploi départemental et sectoriel](https://www.insee.fr/fr/statistiques/1409895?sommaire=1409948) de 1982 à 2013 pour 38 secteurs - INSEE
                      * [Fichier geojson pour la carte des départements](https://france-geojson.gregoiredavid.fr/)
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
                [dash.dependencies.Output('map', 'figure'),
                dash.dependencies.Output('graph', 'figure'),],
                [dash.dependencies.Input('map-type', 'value'),
                dash.dependencies.Input('name', 'value'),
                dash.dependencies.Input('year', 'value'),
                dash.dependencies.Input('secteurs', 'value'),
                dash.dependencies.Input('dpt', 'value'),
                dash.dependencies.Input('sexe', 'value'),
            ])(self.update_graph)

        self.app.callback(
            [dash.dependencies.Output('sheet', 'style'),
             dash.dependencies.Output('secteurs', 'style'),
             dash.dependencies.Output('secteurs', 'options'),
             dash.dependencies.Output('gender', 'style'),
             dash.dependencies.Output('sexe', 'labelStyle'),
             dash.dependencies.Output('name', 'style'),
             dash.dependencies.Output('prenom', 'style'),
             dash.dependencies.Output('departements', 'style'),
             dash.dependencies.Output('dpt', 'style'),
             dash.dependencies.Output('year', 'options'),
             dash.dependencies.Output('year', 'value')
            ],
            [dash.dependencies.Input('map-type', 'value'),]
        )(self.update_map_display)

    def update_map_display(self, mtype):
        """
            Affiche/Cache les options disponibles en fonction du type de carte. 
        """
        display = {'diplay':'block'}
        undisplay = {'display':'None'}
        width = {'width':'9em'}
        sheet = width if mtype == 2 or mtype == 3 else undisplay 
        secteur = {'width': '25em'} if mtype == 2 or mtype == 3 else undisplay
        if mtype == 3:
            options = [{'label': self.secteurs[code],'value': code} for code in self.unique_categories]
        else:
            options = [{'label': description, 'value': code} 
                for code, description in self.secteurs.items()]

        if mtype == 0:
            years = [{'label': i, 'value': i} for i in range(1900, 2021)]
            year_val = 1900
        elif mtype == 1:
            years = [{'label': i, 'value': i} for i in range(1982, 2015)]
            year_val = 1982
        else:
            years = [{'label': i, 'value': i} for i in range(1989, 2014)]
            year_val = 1989


        gender = width if mtype == 2 else undisplay 
        sexe = display if mtype == 2 else undisplay 
        name = width if mtype == 0 or mtype == 3 else undisplay
        prenom = width if mtype == 0 or mtype == 3 else undisplay
        departements = width if mtype != 3 else undisplay
        dpt = width if mtype != 3 else undisplay

        return sheet, secteur, options, gender, sexe, name, prenom, departements, dpt, years, year_val
        
    def update_occ_name_year(self, name, year):
        if name is None or year is None:
            return
        try:
            df = self.prenoms.loc[(slice(None), slice(None), year, name), :].groupby('dpt').sum().reindex(self.dpt, fill_value=0).reset_index()
        except KeyError:
            df = pd.DataFrame(data={'dpt': self.dpt, 'nombre': 0})

        fig = px.choropleth_mapbox(df, geojson=self.departements, locations='dpt', color='nombre',
                               featureidkey='properties.code',
                               color_continuous_scale="Amp",
                               range_color=(0, max(1, df.nombre.max())),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 47, "lon": 2},
                               opacity=0.5,
                               labels={'dpt':'département', 'nombre':'occurence'}
                              )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def plot_name_occurence_france(self, name):
        if name is None:
            return
        df = self.prenoms.loc[(slice(None), slice(None), slice(None), name), :].groupby('annais').sum().reset_index()
        fig = px.line(df, y='nombre', x='annais',
                      markers=True,
                      labels={"nombre":f"naissances des {name}", "annais": "années"},
                      title=f'Historique du prénom {name} dans toute la France')
        return fig

    def plot_name_occurence_departement(self, name, departement):
        if name is None or departement is None:
            return
        df = self.prenoms.loc[(slice(None), departement, slice(None), name), :].groupby('annais').sum().reset_index()
        fig = px.line(df, y='nombre', x='annais',
                      markers=True,
                      labels={"nombre":f"occurences des {name}", "annais": "années"},
                      title=f'Historique du prénom {name} dans le département: {DEPARTMENTS[departement]}',
                      )
        return fig
    
    def update_chomage_year(self, year):
        fig = px.choropleth_mapbox(self.chomage.rename(columns={year: 'Taux de chomage en %'}),
                                   geojson=self.departements, locations='dpt', color='Taux de chomage en %',
                               featureidkey='properties.code',
                               color_continuous_scale="Amp",
                               range_color=(0, 16),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 47, "lon": 2},
                               opacity=0.5,
                               labels={'dpt':'departement', 'Taux de chômage':'chomage'}
                              )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    def plot_emploi_sheet_year(self, sexe, year, secteur):
        if secteur is None or year is None:
            return
        if sexe == 0:
            df = self.all_job_sectors.groupby(level=[1, 2, 3]).sum().loc[(slice(None), year, secteur), :]
        else:
            df = self.all_job_sectors.loc[(sexe, slice(None), year, secteur), :]
        df = df.reset_index('dpt')
        fig = px.choropleth_mapbox(df, geojson=self.departements, locations='dpt', color='nombre',
                               featureidkey='properties.code',
                               color_continuous_scale="Amp",
                               range_color=(0, max(1, df['nombre'].max())),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 47, "lon": 2},
                               opacity=0.5,
                               labels={'dpt':'département', 'nombre':'nombre d\'emplois'}
                              )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def plot_correlation_prenom_emploi(self, name, secteur):
        if name is None or secteur is None:
            return
        dpt_correl_name = get_corr_all_dpt_cat_name(self.all_cat_dict_mixed, self.all_prn_dict_mixed, secteur, name)
        df = pd.DataFrame.from_dict(dpt_correl_name, orient='index').reset_index().rename(columns={'index':'dpt', 0:'correlation'})
        fig = px.choropleth_mapbox(df.fillna(value=0), geojson=self.departements, locations='dpt', color='correlation',
                           featureidkey='properties.code',
                           color_continuous_scale="RdBu_r",
                           range_color=(-1, 1),
                           mapbox_style="carto-positron",
                           zoom=5, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={'dpt':'département', 'correlation':'corrélation'}
                          )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def plot_all_chomage(self):
        nb_departement = len(self.chomage)# il y a 95 départements dans nos données
        chomage_annee = self.chomage.set_index('dpt').sum(axis=0) / nb_departement 
        chomage_annee = chomage_annee.reset_index().rename(columns={'index': 'annee', 0: 'taux de chomage'})
        fig = px.line(chomage_annee, y='taux de chomage', x='annee',
                      markers=True,
                      labels={"taux de chomage":"Taux de chômage", "annee": "années"},
                      title='Historique du taux de chômage en France')
        return fig

    def plot_all_chomage_departement(self, dpt):
        chomage_annee_dpt = self.chomage.set_index('dpt').T[dpt].reset_index().rename(columns={'index': 'annee', dpt: 'taux de chomage'})
        fig = px.line(chomage_annee_dpt, y='taux de chomage', x='annee',
                      markers=True,
                      labels={"taux de chomage":f"Taux de chômage dans le {dpt}", "annee": "années"},
                      title=f'Historique du taux de chômage dans le departement: {DEPARTMENTS[dpt]}')
        return fig

    def plot_all_emploi(self, secteur):
        all_emplois = self.all_job_sectors.loc[(slice(None), slice(None), slice(None), secteur), :].groupby(level=[2, 3]).sum().reset_index('annee')
        fig = px.line(all_emplois, y='nombre', x='annee',
                      markers=True,
                      labels={"nombre":"Nombre d'emplois", "annee": "années"},
                      title=f'Historique du nombre d\'emplois en France dans le secteur suivant: {self.secteurs[secteur]}')
        return fig

    def plot_all_emploi_departement(self, secteur, dpt):
        all_emplois = self.all_job_sectors.loc[(slice(None), dpt, slice(None), secteur), :].groupby(level=[1, 2, 3]).sum().reset_index('annee')
        fig = px.line(all_emplois, y='nombre', x='annee',
                      markers=True,
                      labels={"nombre":"Nombre d'emplois", "annee": "années"},
                      title=f'Historique du nombre d\'emplois dans le département: {DEPARTMENTS[dpt]} \n'
                      f'dans le secteur suivant: {self.secteurs[secteur]}')
        return fig

    def update_graph(self, map_type, name, year, secteur, dpt, sexe):
        name = name.lower() if name != None and map_type == 0 or map_type == 3 else None
        if map_type == 0:
            fig = self.plot_name_occurence_france(name) if dpt==None else self.plot_name_occurence_departement(name, dpt) 
            return self.update_occ_name_year(name, year), fig 
        elif map_type == 1:
            fig = self.plot_all_chomage() if dpt == None else self.plot_all_chomage_departement(dpt)
            return self.update_chomage_year(year), fig 
        elif map_type == 2:
            fig = self.plot_all_emploi(secteur) if dpt==None else self.plot_all_emploi_departement(secteur, dpt)
            return self.plot_emploi_sheet_year(sexe, year, secteur), fig 
        else:
            fig = self.plot_name_occurence_france(name) if dpt==None else self.plot_name_occurence_departement(name, dpt) 
            return self.plot_correlation_prenom_emploi(name, secteur), fig

if __name__ == '__main__':
    nrg = Prenoms()
    nrg.app.run_server(debug=True, port=8051)
