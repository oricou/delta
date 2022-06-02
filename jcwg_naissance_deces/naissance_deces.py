from dash import dcc
from dash import html
import dash
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp


class Naissance():
    def __init__(self, application=None):
        with open('data/jcwg_departements.geojson') as f:
            self.dep = json.load(f)

        # Load pkl
        self.daten = pd.read_pickle('data/jcwg_date_naissance.pkl')
        self.dated = pd.read_pickle('data/jcwg_date_deces.pkl')

        self.depn = pd.read_pickle('data/jcwg_department_naissance.pkl')
        self.depd = pd.read_pickle('data/jcwg_department_deces.pkl')

        self.agen = pd.read_pickle('data/jcwg_age_naissance.pkl')
        self.aged = pd.read_pickle('data/jcwg_age_deces.pkl')

        self.zmax = max(self.depn['SIZE'].max(), self.depd['SIZE'].max())
        self.zmin = min(self.depn['SIZE'].min(), self.depd['SIZE'].min())

        # Set info for graph
        self.tickval = [self.zmin, 1000, 2000, 5000, 10000, 20000, 30000,
                        self.zmax]
        self.date_axis = [pd.to_datetime(d) for d in sorted(set(
            self.daten.reset_index()['date']))]
        self.age_naissances_axis = list(range(17, 46))
        self.age_deces_axis = list(sorted(set(self.aged.reset_index()['AGE'])))
        self.dep_map = {d['properties']['code']: d['properties']['nom']
                        for d in self.dep['features']}
        self.dep_idx_map = {d: i for i, d in enumerate(sorted(self.dep_map))}

        # Double map Naissance/Deces
        self.fig = sp.make_subplots(
            rows=1,
            cols=2,
            subplot_titles=('Naissances', 'Décès'),
            specs=[[{"type": "mapbox"}, {"type": "mapbox"}]],
        )

        # Enable multi-element selection
        self.fig.update_layout(
            clickmode='event+select',
            hovermode='closest',
            margin=dict(l=0, r=0, t=30, b=0),
        )

        self.fig.add_trace(self.create_fig_naissances(), row=1, col=1)
        self.fig.add_trace(self.create_fig_deces(), row=1, col=2)

        self.fig.update_mapboxes(
            style='carto-positron',
            center={"lat": 47.0353, "lon": 2.2928},
            zoom=4.42,
        )

        # main layout
        self.main_layout = html.Div(children=[
            html.H3(children='Naissance et décès en France en 2019'),

            # Map div.
            html.Div([
                dcc.Graph(
                    id='map',
                    figure=self.fig,
                    style={'width': '100%', 'display': 'inline-block'},
                )
            ],
                style={
                    'display': 'flex',
                    'justifycontent': 'center',
                }
            ),

            # List of department name.
            html.Div([
                html.Plaintext(id='list_department',
                               style={
                                   'width': '50%',
                                   'whiteSpace': 'normal',
                                   'height': 'auto',
                                   'overflow-wrap': 'break-word',
                               }),
            ],
                style={
                    'display': 'flex',
                    'justifycontent': 'center',
                    'height': 'auto',
                }
            ),

            html.Br(),

            # Double graph with Naissance/Deces
            html.Div([
                dcc.Graph(id='size_france',
                          style={'width': '95%', 'display': 'inline-block'}),
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id='wps-naissance-deces-1',
                        options=[{'label': i, 'value': i} for i in
                                 ['Naissance', 'Décès']],
                        value=['Naissance', 'Décès'],
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                    html.Br(),
                    dcc.RadioItems(
                        id='wps-uni-mg-1',
                        options=[{'label': i, 'value': i} for i in
                                 ['Unitaire', 'Moyenne', ]],
                        value='Moyenne',
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                ], style={'width': '10%', 'display': 'inline-block'}),
            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'justifyContent': 'center', }),
            html.Br(),

            html.Div([
                dcc.Graph(id='size_naissance',
                          style={'width': '90%', 'display':
                              'inline-block', }),
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id='wps-hf-2',
                        options=[{'label': i, 'value': i} for i in
                                 ['Femme', 'Homme', 'Somme', 'Moyenne']],
                        value=['Femme', 'Homme'],
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                    html.Br(),
                    dcc.RadioItems(
                        id='wps-uni-mg-2',
                        options=[{'label': i, 'value': i} for i in
                                 ['Unitaire', 'Moyenne', ]],
                        value='Moyenne',
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                ], style={'width': '10%', 'display': 'inline-block', }),

                dcc.Graph(id='size_deces',
                          style={'width': '90%',
                                 'display': 'inline-block', }),

                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id='wps-hf-3',
                        options=[{'label': i, 'value': i} for i in
                                 ['Femme', 'Homme', 'Somme', 'Moyenne']],
                        value=['Femme', 'Homme'],
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                    html.Br(),
                    dcc.RadioItems(
                        id='wps-uni-mg-3',
                        options=[{'label': i, 'value': i} for i in
                                 ['Unitaire', 'Moyenne', ]],
                        value='Moyenne',
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                ], style={'width': '10%', 'display': 'inline-block'}),

            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'borderBottom': 'thin lightgrey solid',
                      'justifyContent': 'center', }),
            html.Br(),
            dcc.Markdown("""
            Les cartes sont interactives. En passant la souris sur les départements vous avez une infobulle.
            De plus, en sélectionnant plusieurs départements (shift et clic), on peut avoir plus d'info sur ceux-ci à l'aide des graphiques.
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la carte, réinitialiser avec un double clic et utiliser le lasso pour sélectionner plusieurs départements.

            #### Informations intéressantes :
               * On remarque que les grosses villes ont un important nombre de naissances et un plus faible nombre de décès.
                Avec l'âge les gens finissent leur vie en régions plutôt que dans les grandes villes.
               * Cela se confirme en étudiant les départements unitairement, les zones à forte population ont plus de naissances que de décès.
                On observe le phénomène inverse dans les départements moins peuplés.
               * On observe une croissance démographique en France, il y a plus de naissances que de décès.
               * On repère les hivers avec un nombre plus important de mort durant ces périodes.
               * On observe moins de naissances de février à avril, pour un pic de naissances en juillet.
               * Les hommes ont en moyenne des enfants plus tard que les femmes.
               * Les femmes vivent plus longtemps que les hommes.

            #### À propos

            * Sources : https://www.data.gouv.fr/fr/datasets/population/
            * (c) 2022 William Grolleau, Jeremy Croiset.
            """)
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        })

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Update subgraph when the selected department are updated.
        self.app.callback(
            dash.dependencies.Output('size_france', 'figure'),
            dash.dependencies.Input('map', 'selectedData'),
            dash.dependencies.Input('wps-naissance-deces-1', 'value'),
            dash.dependencies.Input('wps-uni-mg-1', 'value'),
        )(self.size_france)
        self.app.callback(
            dash.dependencies.Output('size_naissance', 'figure'),
            dash.dependencies.Input('map', 'selectedData'),
            dash.dependencies.Input('wps-uni-mg-2', 'value'),
            dash.dependencies.Input('wps-hf-2', 'value'),
        )(self.size_naissance)
        self.app.callback(
            dash.dependencies.Output('size_deces', 'figure'),
            dash.dependencies.Input('map', 'selectedData'),
            dash.dependencies.Input('wps-uni-mg-3', 'value'),
            dash.dependencies.Input('wps-hf-3', 'value'),
        )(self.size_deces)

        # Update list of department names upon map selection.
        self.app.callback(
            dash.dependencies.Output('list_department', 'children'),
            dash.dependencies.Input('map', 'selectedData'),
        )(self.list_dep)

        # Sync mapboxes layout and selection.
        self.app.callback(
            dash.dependencies.Output('map', 'figure'),
            dash.dependencies.Input('map', 'relayoutData'),
            dash.dependencies.Input('map', 'selectedData'),
        )(self.map_sync)

    def get_mapbox_layout_params(self, relayout_data):
        """Get the layout data from any mapbox in the figure.

        :param relayout_data: Update relayout of the map
        :return: dict of the relayout data sanitized.
        """
        keys = ['center', 'zoom', 'bearing', 'pitch']

        params = dict()
        for data_key in relayout_data.keys():
            params.update({ k: relayout_data[data_key] for k in keys if k in data_key })

        return params

    def map_sync(self, relayout_data, selected_data):
        """Update the layout and selection of other maps.

        :param relayout_data: layout of the updated map.
        :param selected_data: select data of the updated map.
        :return: New figure with all maps synced.
        """
        deps = self.get_department(selected_data)

        # upate selected elements to reflect on both maps
        self.fig.update_traces(
            selectedpoints=[self.dep_idx_map[d] for d in deps])

        if relayout_data is not None:
            params = self.get_mapbox_layout_params(relayout_data)

            # update layout to reflect on both maps
            self.fig.update_mapboxes(params)

        return self.fig

    def list_dep(self, selected_data):
        """List the department selected, if all are selected return
        'Toute la France'

        :param selected_data: selected data on the map.
        :return: String of departments.
        """
        deps = self.get_department(selected_data)

        if len(deps) == 96:
            return 'Toute la France'
        else:
            return ', '.join([self.dep_map[d] for d in deps])

    def create_fig_naissances(self):
        """Setup `Naissances` figure.

        :return: new figure
        """
        return go.Choroplethmapbox(
            geojson=self.dep,
            name='',
            colorscale='Inferno',
            colorbar=dict(
                tickvals=[np.log10(i) for i in self.tickval],
                ticktext=self.tickval,
                thickness=20,
                x=0.46,
            ),
            locations=self.depn.index,
            customdata=np.stack((self.depn['NAME'], self.depn.index,
                                 self.depn['SIZE']),
                                axis=1),
            hovertemplate=
            "<b>Departement : %{customdata[1]}</b><br><br>" +
            "Nom : %{customdata[0]}<br>" +
            "Naissance : %{customdata[2]}<br>",
            z=np.log10(self.depn['SIZE']),
            zmin=np.log10(self.zmin),
            zmax=np.log10(self.zmax),
        )

    def create_fig_deces(self):
        """Setup `Décès` figure.

        :return: new figure
        """
        return go.Choroplethmapbox(
            geojson=self.dep,
            name='',
            colorscale='Inferno',
            colorbar=dict(
                tickvals=[np.log10(i) for i in self.tickval],
                ticktext=self.tickval,
                thickness=20,
                x=0.46,
            ),
            locations=self.depd.index,
            customdata=np.stack((self.depd['NAME'], self.depd.index,
                                 self.depd['SIZE']),
                                axis=1),
            hovertemplate=
            "<b>Departement : %{customdata[1]}</b><br><br>" +
            "Nom : %{customdata[0]}<br>" +
            "Décès : %{customdata[2]}<br>",
            z=np.log10(self.depd['SIZE']),
            zmin=np.log10(self.zmin),
            zmax=np.log10(self.zmax),
        )

    def get_department(self, selected_data):
        """Get department id of all selected departments. By default, return
        every department in France.

        :param selected_data: selected department data.
        :return: List of department id.
        """
        if selected_data is None or selected_data['points'] == []:
            return list(self.dep_map.keys())
        return [p['location'] for p in selected_data['points']]

    def size_france(self, selected_data, unit_mean, type):
        """Graph about size of Naissance and Deces of every department.

        :param selected_data: selected department.
        :param unit_mean: 'Naissance' or 'Deces'.
        :param type: 'Unitaire' or 'Moyenne'.
        :return: figure of the graph.
        """
        deps = self.get_department(selected_data)

        what = []
        if type == 'Unitaire':
            if 'Naissance' in unit_mean:
                what += [(d, self.daten, 'SIZE', 'Naissance ' +
                          self.dep_map[d])
                         for d in deps]

            if 'Décès' in unit_mean:
                what += [(d, self.dated, 'SIZE',
                          'Décès ' + self.dep_map[d])
                         for d in deps]
        else:
            if 'Naissance' in unit_mean:
                data = self.daten.loc[deps].reset_index().groupby(
                    ['date']).sum()
                what += [(None, data, 'SIZE', 'Naissance cumulée')]
            if 'Décès' in unit_mean:
                data = self.dated.loc[deps].reset_index().groupby(
                    ['date']).sum()
                what += [(None, data, 'SIZE', 'Décès cumulé')]

        return self.cts(self.date_axis, what,
                        "Nombre de naissance et décès par mois")

    def size_naissance(self, selected_data, unit_mean, type):
        """Graph about parents age when they have a child of every department.

        :param selected_data: selected department.
        :param unit_mean: 'Naissance' or 'Deces'.
        :param type: 'Homme, 'Femme, 'Unitaire' or 'Moyenne'.
        :return: figure of the graph.
        """
        dep = self.get_department(selected_data)
        what = []

        if unit_mean == 'Unitaire':
            if 'Femme' in type:
                what += [(d, self.agen, 'SIZEMEREN', 'Femme ' +
                          self.dep_map[d]) for d in dep]
            if 'Homme' in type:
                what += [(d, self.agen, 'SIZEPEREN', 'Homme ' +
                          self.dep_map[d]) for d in dep]
            if 'Somme' in type:
                what += [(d, self.agen, 'SIZEMEREPEREN', 'Somme H/F ' +
                          self.dep_map[d]) for d in dep]
            if 'Moyenne' in type:
                what += [(d, self.agen, 'MGMEREPEREN', 'Moyenne H/F ' +
                          self.dep_map[d]) for d in dep]

        else:
            data = self.agen.loc[dep].reset_index().groupby(['level_1']).sum()
            if 'Femme' in type:
                what += [(None, data, 'SIZEMEREN', 'Total femmes')]
            if 'Homme' in type:
                what += [(None, data, 'SIZEPEREN', 'Total hommes')]
            if 'Somme' in type:
                what += [(None, data, 'SIZEMEREPEREN', 'Total H/F')]
            if 'Moyenne' in type:
                what += [(None, data, 'MGMEREPEREN', 'Moyenne H/F')]

        return self.cts(self.age_naissances_axis, what,
                        "Nombre de naissance en fonction de l'age")

    def size_deces(self, selected_data, unit_mean, type):
        """Graph about age of death of male and female of every department.

        :param selected_data: selected department.
        :param unit_mean: 'Naissance' or 'Deces'.
        :param type: 'Homme, 'Femme, 'Unitaire' or 'Moyenne'.
        :return: figure of the graph.
        """
        dep = self.get_department(selected_data)
        what = []

        if unit_mean == 'Unitaire':
            if 'Femme' in type:
                what += [(d, self.aged, 'SIZEMERED', 'Femme ' +
                          self.dep_map[d]) for d in dep]
            if 'Homme' in type:
                what += [(d, self.aged, 'SIZEPERED', 'Homme ' +
                          self.dep_map[d]) for d in dep]
            if 'Somme' in type:
                what += [(d, self.aged, 'SIZEMEREPERED', 'Somme H/F ' +
                          self.dep_map[d]) for d in dep]
            if 'Moyenne' in type:
                what += [(d, self.aged, 'MGMEREPERED', 'Moyenne H/F ' +
                          self.dep_map[d]) for d in dep]
        else:
            data = self.aged.loc[dep].reset_index().groupby(['AGE']).sum()
            if 'Femme' in type:
                what += [(None, data, 'SIZEMERED', 'Total femmes')]
            if 'Homme' in type:
                what += [(None, data, 'SIZEPERED', 'Total hommes')]
            if 'Somme' in type:
                what += [(None, data, 'SIZEMEREPERED', 'Total H/F')]
            if 'Moyenne' in type:
                what += [(None, data, 'MGMEREPERED', 'Moyenne H/F')]

        return self.cts(self.age_deces_axis, what,
                        "Nombre de décès en fonction de l'age")

    def cts(self, x_axis, what, title):
        scatters = []
        for dep, dataframe, w, name in what:
            scatters.append(go.Scatter(
                x=x_axis,
                y=dataframe[w] if dep is None else dataframe.loc[dep][w],
                name=name,
                mode='lines+markers',
            ))

        return {
            'data': scatters,
            'layout': {
                'height': 300,
                'margin': {'l': 50, 'b': 30, 'r': 10, 't': 70},
                'yaxis': {'type': 'linear',
                          'font': {'size': 15}},
                'title': {'text': title,
                          'font': {'size': 15}},
                'legend': {
                    'title': {'font': {'size': 5}},
                    'font': {'size': 11}},
                'xaxis': {'showgrid': False},
                'font': {'size': 10},
            }
        }


if __name__ == '__main__':
    mpj = Naissance()
    mpj.app.run_server(debug=True, port=8051)
