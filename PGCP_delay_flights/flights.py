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


class Delay():
    dico = {1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin', 7: 'juillet',
            8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre', }

    def __init__(self, application=None):

        data1 = pd.read_csv('data/flights0.csv')
        data2 = pd.read_csv('data/flights1.csv')
        data = pd.concat([data1, data2])
        data = data[['MONTH', 'DAY_OF_MONTH', 'STATE_NAME', 'DEP_DELAY_NEW', 'CANCELLED']]
        data_graph2 = data[['MONTH', 'DAY_OF_MONTH', 'DEP_DELAY_NEW', 'CANCELLED']]

        def cutStateName(df):
            infos = df['ORIGIN_CITY_NAME'].split(', ')
            return infos[1]

        def makeDate(df):
            month = df['MONTH']
            day = df['DAY_OF_MONTH']
            month = '0' + str(month) if month < 10 else str(month)
            day = '0' + str(day) if day < 10 else str(day)
            return '2019-' + month + '-' + day

        data['DATE'] = data.apply(makeDate, axis=1)

        dico = {1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin', 7: 'juillet',
                8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre', }

        self.df = data
        self.df2 = data_graph2

        self.main_layout = html.Div(children=[
            html.Div([
            html.H3(children='Retards et annulations des vols aux Etats-Unis en 2019', style={'text-align': 'center', 'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '30px', 'fill':'rgb(42, 63, 95)'}),
            html.Div([dcc.Markdown("Cette page présente 2 graphiques pour tenter de montrer en quoi le retard voire l'annulation d'un vol aux Etats-Unis peuvent être impactés par le lieu d'origine du vol et par la période de temps en 2019.")], style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '20px', 'fill':'rgb(42, 63, 95)'}),
            html.Div([dcc.Graph(id='map-graph'), ], style={'width': '100%', }),
            html.Div([
                html.Div([html.Div('Status'),
                          dcc.RadioItems(
                              id='status-type',
                              options=[{'label': 'Retardé', 'value': 'delayed'},
                                       {'label': 'Annulé', 'value': 'cancelled'}, ],
                              value='delayed',
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '9em'}),
                html.Div([html.Div('Mois ref.'),
                          dcc.Dropdown(
                              id='which-month',
                              options=[{'label': dico[i], 'value': i} for i in range(1, 13)],
                              value=1,
                              disabled=True,
                          ),
                          ], style={'width': '6em', 'padding': '2em 0px 0px 0px'}),  # bas D haut G
                html.Div([html.Div('Jour ref.'),
                          dcc.Dropdown(
                              id='which-day',
                              options=[{'label': i, 'value': i} for i in range(1, 31)],
                              value=1,
                              disabled=True,
                          ),
                          ], style={'width': '6em', 'padding': '2em 0px 0px 0px'}),
                html.Div(style={'width': '2em'}),
                html.Div([html.Div('Échelle de temps'),
                          dcc.RadioItems(
                              id='time-type',
                              options=[{'label': 'Jour', 'value': 'day'},
                                       {'label': 'Mois', 'value': 'month'},
                                       {'label': 'Tous les mois', 'value': 'year'},
                                       {'label': "A l'année", 'value': 'absolute'},
                                       {'label': 'Tous les jours', 'value': 'all'}],
                              value='absolute',
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '15em', 'margin': "0px 0px 0px 40px"}),  # bas D haut G
            ], style={
                'padding': '10px 50px',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'flex-start',
            }),
            html.Br(),
            dcc.Markdown("On peut observer sur la carte que les états de l'est des Etats-Unis ont tendance à avoir une plus grande moyenne de retards de vols comparé aux états de l'ouest", style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '20px', 'fill':'rgb(42, 63, 95)'})
            ]),
            html.Div([
            html.Div([dcc.Graph(id='graph'), ], style={'width': '100%', }),
            html.Div([
                html.Div([html.Div('Status'),
                          dcc.RadioItems(
                              id='status',
                              options=[{'label': 'Retardé', 'value': 'delayed'},
                                       {'label': 'Annulé', 'value': 'cancelled'}, ],
                              value='delayed',
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '9em'}),
                html.Div([html.Div('Rapport'),
                          dcc.RadioItems(
                              id='status_info',
                              options=[{'label': 'Temps', 'value': 'Temps'},
                                       {'label': 'Nombre','value':'nombre'}],
                              value='nombre',

                          ),
                          ], style={'width': '9em'}),  # bas D haut G
                html.Div([html.Div('Mois ref.'),
                          dcc.Dropdown(
                              id='month_id',
                              options=[{'label': dico[i], 'value': i} for i in range(1, 13)],
                              value=1,
                              disabled=True,
                          ),
                          ], style={'width': '6em', 'padding': '2em 0px 0px 0px'}),
                html.Div(style={'width': '2em'}),
                html.Div([html.Div('Échelle de temps'),
                          dcc.RadioItems(
                              id='time',
                              options=[{'label': 'Mois', 'value': 'month'},
                                       {'label': 'Année', 'value': 'year'},
                                       ],
                              value='year',
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '15em', 'margin': "0px 0px 0px 40px"}),  # bas D haut G
            ], style={
                'padding': '10px 50px',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'flex-start',
            }),
            html.Br(),
            dcc.Markdown("On peut voir sur le graphique que les mois de juillet et août observent un plus grand nombre de vols retardés. Cela peut être expliqué par l'affluence des départs/retours de vacances.", style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '20px', 'fill':'rgb(42, 63, 95)'}),
            dcc.Markdown("Le mois de décembre observe un pic dans le nombre de vols retardés entre le 20 et le 25. Cela peut s'expliquer par la forte affluence en période de Noël.", style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '20px', 'fill':'rgb(42, 63, 95)'}),
            html.Br(),
            dcc.Markdown("A propos", style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '30px', 'fill':'rgb(42, 63, 95)'}),
            dcc.Markdown("Sources: https://www.kaggle.com/code/threnjen/dataset-cleanup-how-the-train-test-sets-were-made/data?select=raw_data", style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '20px', 'fill':'rgb(42, 63, 95)'}),
            dcc.Markdown("(c) 2022 Corentin Pion & Paul Grolier", style={'font-family': '"Open Sans", verdana, arial, sans-serif', 'font-size': '14px', 'fill':'rgb(42, 63, 95)'})
        ])
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
            dash.dependencies.Output('map-graph', 'figure'),
            [dash.dependencies.Input('status-type', 'value'),
             dash.dependencies.Input('time-type', 'value'),
             dash.dependencies.Input('which-month', 'value'),
             dash.dependencies.Input('which-day', 'value')])(self.makeMap)
        self.app.callback(
            [dash.dependencies.Output('which-month', 'disabled'),
             dash.dependencies.Output('which-day', 'disabled')],
            dash.dependencies.Input('time-type', 'value'))(self.disable_month_year)
        self.app.callback(
            dash.dependencies.Output('graph', 'figure'),
            [dash.dependencies.Input('status', 'value'),
             dash.dependencies.Input('status_info', 'value'),
             dash.dependencies.Input('month_id', 'value'),
             dash.dependencies.Input('time', 'value')])(self.Delay_time)
        self.app.callback(
            dash.dependencies.Output('month_id', 'disabled'),
            dash.dependencies.Input('time','value'))(self.disable_time)

    def makeMap(self, state='delayed', timeline='all', month=1, day=1):
        data_delay = self.df.drop(['CANCELLED'], axis=1)
        data_delay = self.df[self.df['DEP_DELAY_NEW'] > 0.]

        data_cancel = self.df.drop(['DEP_DELAY_NEW'], axis=1)
        data_fly = self.df[self.df['CANCELLED'] == 0.]
        data_cancel = self.df[self.df['CANCELLED'] == 1.]

        if timeline == 'day':
            if state == 'cancelled':
                data_cancel = data_cancel[(data_cancel['MONTH'] == month) & (data_cancel['DAY_OF_MONTH'] == day)]

                data_cancel = data_cancel.groupby(['STATE_NAME']).agg({'CANCELLED': ['count']})
                data_cancel.columns = ['CANCELLED_COUNT']
                data_cancel = data_cancel.reset_index()

                data_fly = data_fly.groupby(['STATE_NAME']).agg({'CANCELLED': ['count']})
                data_fly.columns = ['FLYING_COUNT']
                data_fly = data_fly.reset_index()

                data_cancel = pd.merge(data_cancel, data_fly, on=['STATE_NAME'])
                data_cancel['CANCELLED_RATIO'] = data_cancel['CANCELLED_COUNT'] / data_cancel['FLYING_COUNT'] * 100

                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='CANCELLED_RATIO',
                                    labels={'CANCELLED_RATIO': 'Pourcentage de vols annulés'}, hover_name='STATE_NAME',
                                    hover_data={'STATE_NAME': False}, color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état le " + str(day) + ' ' + self.dico[
                                        month] + ' 2019')
            else:
                data_delay = data_delay[(data_delay['MONTH'] == month) & (data_delay['DAY_OF_MONTH'] == day)]

                data_delay = data_delay.groupby(['STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()

                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='DELAY_MEAN',
                                    labels={'DELAY_MEAN': 'Retard moyen'}, hover_name='STATE_NAME',
                                    hover_data={'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état le " + str(day) + ' ' + self.dico[
                                        month] + ' 2019')

        elif timeline == 'month':
            if state == 'cancelled':
                data_cancel = data_cancel[data_cancel['MONTH'] == month]

                data_cancel = data_cancel.groupby(['DAY_OF_MONTH', 'STATE_NAME']).agg({'CANCELLED': ['count']})
                data_cancel.columns = ['CANCELLED_COUNT']
                data_cancel = data_cancel.reset_index()

                data_fly = data_fly.groupby(['DAY_OF_MONTH', 'STATE_NAME']).agg({'CANCELLED': ['count']})
                data_fly.columns = ['FLYING_COUNT']
                data_fly = data_fly.reset_index()

                data_cancel = pd.merge(data_cancel, data_fly, on=['DAY_OF_MONTH', 'STATE_NAME'])
                data_cancel['CANCELLED_RATIO'] = data_cancel['CANCELLED_COUNT'] / data_cancel['FLYING_COUNT'] * 100

                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='CANCELLED_RATIO',
                                    animation_frame='DAY_OF_MONTH',
                                    labels={'CANCELLED_RATIO': 'Pourcentage de vols annulés', 'DAY_OF_MONTH': 'jour'},
                                    hover_name='STATE_NAME', hover_data={'DAY_OF_MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état en " + self.dico[month] + ' 2019')
            else:
                data_delay = data_delay[data_delay['MONTH'] == month]

                data_delay = data_delay.groupby(['DAY_OF_MONTH', 'STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()

                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='DELAY_MEAN',
                                    animation_frame='DAY_OF_MONTH',
                                    labels={'DELAY_MEAN': 'Retard moyen', 'DAY_OF_MONTH': 'jour'},
                                    hover_name='STATE_NAME', hover_data={'DAY_OF_MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état en " + self.dico[month] + ' 2019')

        elif timeline == 'year':
            if state == 'cancelled':
                data_cancel = data_cancel.groupby(['MONTH', 'STATE_NAME']).agg({'CANCELLED': ['count']})
                data_cancel.columns = ['CANCELLED_COUNT']
                data_cancel = data_cancel.reset_index()

                data_fly = data_fly.groupby(['MONTH', 'STATE_NAME']).agg({'CANCELLED': ['count']})
                data_fly.columns = ['FLYING_COUNT']
                data_fly = data_fly.reset_index()

                data_cancel = pd.merge(data_cancel, data_fly, on=['MONTH', 'STATE_NAME'])
                data_cancel['CANCELLED_RATIO'] = data_cancel['CANCELLED_COUNT'] / data_cancel['FLYING_COUNT'] * 100

                # data_cancel["MONTH"] = data_cancel["MONTH"].map(lambda x :self.dico["MONTH"][x])
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='CANCELLED_RATIO',
                                    animation_frame='MONTH',
                                    labels={'CANCELLED_RATIO': 'Pourcentage de vols annulés', 'MONTH': 'mois'},
                                    hover_name='STATE_NAME', hover_data={'MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état et par mois en 2019")
            else:
                data_delay = data_delay.groupby(['MONTH', 'STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                # data_delay["MONTH"] = data_delay["MONTH"].map(lambda x :self.dico["MONTH"][x])
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='DELAY_MEAN',
                                    animation_frame='MONTH', labels={'DELAY_MEAN': 'Retard moyen', 'MONTH': 'mois'},
                                    hover_name='STATE_NAME',
                                    hover_data={'MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état et par mois en 2019")

        elif timeline == 'absolute':
            if state == 'cancelled':
                data_cancel = data_cancel.groupby(['STATE_NAME']).agg({'CANCELLED': ['count']})
                data_cancel.columns = ['CANCELLED_COUNT']
                data_cancel = data_cancel.reset_index()

                data_fly = data_fly.groupby(['STATE_NAME']).agg({'CANCELLED': ['count']})
                data_fly.columns = ['FLYING_COUNT']
                data_fly = data_fly.reset_index()

                data_cancel = pd.merge(data_cancel, data_fly, on=['STATE_NAME'])
                data_cancel['CANCELLED_RATIO'] = data_cancel['CANCELLED_COUNT'] / data_cancel['FLYING_COUNT'] * 100

                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='CANCELLED_RATIO',
                                    labels={'CANCELLED_RATIO': 'Pourcentage de vols annulés'}, hover_name='STATE_NAME',
                                    hover_data={'STATE_NAME': False}, color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état en 2019")
            else:
                data_delay = data_delay.groupby(['STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()

                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='DELAY_MEAN',
                                    labels={'DELAY_MEAN': 'Retard moyen'}, hover_name='STATE_NAME',
                                    hover_data={'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état en 2019")

        else:
            if state == 'cancelled':
                data_cancel = data_cancel.groupby(['DATE', 'STATE_NAME']).agg({'CANCELLED': ['count']})
                data_cancel.columns = ['CANCELLED_COUNT']
                data_cancel = data_cancel.reset_index()

                data_fly = data_fly.groupby(['DATE', 'STATE_NAME']).agg({'CANCELLED': ['count']})
                data_fly.columns = ['FLYING_COUNT']
                data_fly = data_fly.reset_index()

                data_cancel = pd.merge(data_cancel, data_fly, on=['DATE', 'STATE_NAME'])
                data_cancel['CANCELLED_RATIO'] = data_cancel['CANCELLED_COUNT'] / data_cancel['FLYING_COUNT'] * 100
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='CANCELLED_RATIO',
                                    animation_frame='DATE', labels={'CANCELLED_RATIO': 'Pourcentage de vols annulés'},
                                    hover_name='STATE_NAME', hover_data={'DATE': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état et par jour en 2019")
            else:
                data_delay = data_delay.groupby(['DATE', 'STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa',
                                    color='DELAY_MEAN',
                                    animation_frame='DATE', labels={'DELAY_MEAN': 'Retard moyen'},
                                    hover_name='STATE_NAME',
                                    hover_data={'DATE': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état et par jour en 2019")

        return fig

    def month_all(self, status='delayed', delay_info='nombre', month=1):
        # Ce bloque ce retrouveras pas ici pour apres
        indexNames = self.df2[self.df2['MONTH'] != month].index
        bdd = self.df2.copy()
        bdd.drop(indexNames, inplace=True)
        data_delay = bdd.drop(['CANCELLED'], axis=1)
        data_delay = data_delay[data_delay['DEP_DELAY_NEW'] > 0.]

        data_cancel = bdd.drop(['DEP_DELAY_NEW'], axis=1)
        data_cancel = data_cancel[data_cancel['CANCELLED'] == 1.]
        if status == 'delayed':
            # Calcule en fonction du temps du delay
            if delay_info == 'Temps':
                dd_m_t = data_delay.groupby(['DAY_OF_MONTH']).agg({'DEP_DELAY_NEW': ['mean']})
                dd_m_t.columns = ['mean']
                dd_m_t = dd_m_t.reset_index()
                titre = "Delai moyen d'un avion pour le moi de " + self.dico["MONTH"]
                figure = px.bar(dd_m_t, x="DAY_OF_MONTH", y="mean",
                             labels={'mean': "Delai moyen", 'DAY_OF_MONTH': self.dico["MONTH"]}, text_auto='.2s', title=titre)
            # Calcule en fonction du nombre de delay
            else:
                dd = data_delay.assign(Value=[1] * data_delay.shape[0])
                dd_m_n = dd.groupby(['DAY_OF_MONTH']).agg({'Value': ['sum']})
                dd_m_n.columns = ['Sum']
                dd_m_n = dd_m_n.reset_index()
                # dd_y_n['MONTH'] = dd_y_n.apply(showMeTheMonth, axis=1)
                titre = "Nombre d'avion ayant un delai pour le moi de  " + self.dico[month]
                figure = px.bar(dd_m_n, x="DAY_OF_MONTH", y="Sum",
                             labels={'Sum': "Nombre d'avion ayant un délai", 'DAY_OF_MONTH': self.dico[month]},
                             text_auto='.2s', title=titre)

        elif status == 'cancelled':
            dc = data_cancel.assign(Value=[1] * data_cancel.shape[0])
            dc_m = dc.groupby(['DAY_OF_MONTH']).agg({'Value': ['sum']})
            dc_m.columns = ['Sum']
            dc_m = dc_m.reset_index()
            # dc_y['MONTH'] = dc_y.apply(showMeTheMonth, axis=1)
            titre = "Nombre d'avion annulé pour le moi de  " + self.dico[month]
            figure = px.bar(dc_m, x="DAY_OF_MONTH", y="Sum",
                         labels={'Sum': "Nombre d'avion annulés", 'DAY_OF_MONTH': self.dico[month]}, text_auto='.2s',
                         title=titre)

        else:
            # for both - create a column status and drop if delay ==0 anda canceled == 0
            data_both = self.df2[(self.df2['DEP_DELAY_NEW'] > 0.) | (self.df2['CANCELLED'] == 1.)]
            # Transformation data
            data_both_status = data_both.copy()
            data_both_status['Status'] = ['Delay' if x > 0. else 'Cancelled' for x in data_both_status['DEP_DELAY_NEW']]
            data_both_status['Value'] = [1] * data_both_status.shape[0]
            df_b = data_both_status.groupby(['DAY_OF_MONTH', 'Status']).agg({'Value': ['sum']})
            df_b.columns = ['Sum']
            df_b = df_b.reset_index()
            # figure
            titre = "Nombre d'avion annulé et presentant un delai pour le moi de  " + self.dico[month]
            figure = px.bar(df_b, x='DAY_OF_MONTH', y='Sum', color='Status',
                         labels={'Sum': "Nombre d'avion possedant un délai et/ou annulés", 'DAY_OF_MONTH': self.dico[month]},
                         text_auto='.2s', title=titre)
        return figure

    def Delay_time(self, status='delayed', delay_info='nombre', month=1, time='year'):
        data_delay = self.df2.drop(['CANCELLED'], axis=1)
        data_delay = data_delay[data_delay['DEP_DELAY_NEW'] > 0.]
        data_cancel = self.df2.drop(['DEP_DELAY_NEW'], axis=1)
        data_cancel = data_cancel[data_cancel['CANCELLED'] == 1.]
        # if Both is used we use the same dataframe because we need canceled and delayed
        if time == 'month':
            figur =  self.month_all(status, delay_info, month)
        else:
            if status == 'delayed':
                # Calcule en fonction du temps du delay
                if delay_info == 'Temps':
                    dd_y_t = data_delay.groupby(['MONTH']).agg({'DEP_DELAY_NEW': ['mean']})
                    dd_y_t.columns = ['mean']
                    dd_y_t = dd_y_t.reset_index()
                    #dd_y_t['MONTH'] = dd_y_t.apply(showMeTheMonth, axis=1)
                    titre = "Delai moyen enregistre par mois sur l'année 2019"
                    figur = px.bar(dd_y_t, x="MONTH", y="mean", labels={'mean': "Delai moyen", 'MONTH': "Année 2019"},
                                 text_auto='.2s', title=titre)
                # Calcule en fonction du nombre de delay
                else:
                    dd = data_delay.assign(Value=[1] * data_delay.shape[0])
                    dd_y_n = dd.groupby(['MONTH']).agg({'Value': ['sum']})
                    dd_y_n.columns = ['Sum']
                    dd_y_n = dd_y_n.reset_index()
                    #dd_y_n['MONTH'] = dd_y_n.apply(showMeTheMonth, axis=1)
                    titre = "Nombre d'avion presentant un delai par mois sur l'année 2019"
                    figur = px.bar(dd_y_n, x="MONTH", y="Sum", labels={'Sum': "Nombre de délai", 'MONTH': "Année 2019"},
                                 text_auto='.2s', title=titre)

            elif status == 'cancelled':
                dc = data_cancel.assign(Value=[1] * data_cancel.shape[0])
                dc_y = dc.groupby(['MONTH']).agg({'Value': ['sum']})
                dc_y.columns = ['Sum']
                dc_y = dc_y.reset_index()
                #dc_y['MONTH'] = dc_y.apply(showMeTheMonth, axis=1)
                titre = "Nombre d'avion annulé par mois sur l'année 2019"
                figur = px.bar(dc_y, x="MONTH", y="Sum", labels={'Sum': "Nombre d'annulation", 'MONTH': "Année 2019"},
                             text_auto='.2s', title=titre)

            else:
                # for both - create a column status and drop if delay ==0 anda canceled == 0
                data_both = self.df2[(self.df2['DEP_DELAY_NEW'] > 0.) | (self.df2['CANCELLED'] == 1.)]
                # Transformation data
                data_both_status = data_both.copy()
                data_both_status['Status'] = ['Delay' if x > 0. else 'Cancelled' for x in
                                              data_both_status['DEP_DELAY_NEW']]
                data_both_status['Value'] = [1] * data_both_status.shape[0]
                df_b = data_both_status.groupby(['MONTH', 'Status']).agg({'Value': ['sum']})
                df_b.columns = ['Sum']
                df_b = df_b.reset_index()
                #df_b['MONTH'] = df_b.apply(showMeTheMonth, axis=1)
                # figure
                titre = "Nombre d'avion annulé et/ou presentant un delai par mois sur l'année 2019"
                figur = px.bar(df_b, x='MONTH', y='Sum', color='Status',
                             labels={'Sum': "Nombre d'annulation et de delai", 'MONTH': "Année 2019"}, text_auto='.2s',
                             title=titre)
        return figur

    def disable_month_year(self, type_jour):
        if type_jour == 'day':
            return False, False
        elif type_jour == 'month':
            return False, True
        else:
            return True, True

    def disable_time(self, time):
        if time == 'month':
            return False
        else:
            return True

if __name__ == '__main__':
    nrg = Delay()
    nrg.app.run_server(debug=True, port=80)
