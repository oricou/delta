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

    def __init__(self, application = None):

        data1 = pd.read_csv('data/flights0.csv')
        data2 = pd.read_csv('data/flights1.csv')
        data = pd.concat([data1, data2])

        data = data[['MONTH', 'DAY_OF_MONTH', 'ORIGIN_CITY_NAME', 'DEP_DELAY_NEW', 'CANCELLED']]


        def cutStateName(df):
            infos = df['ORIGIN_CITY_NAME'].split(', ')
            return infos[1]

        data['ORIGIN_CITY_NAME'] = data.apply(cutStateName, axis=1)
        data = data.rename(columns={'ORIGIN_CITY_NAME': 'STATE_NAME'})

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

        self.main_layout = html.Div(children=[
            html.H3(children='Retards et annulations des vols aux Etats-Unis en 2019'),
            html.Div([ dcc.Graph(id='map-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Status'),
                           dcc.RadioItems(
                               id='status-type',
                               options=[{'label':'Retardé', 'value':'delayed'}, 
                                        {'label':'Annulé','value':'cancelled'},],
                               value='delayed',
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                html.Div([ html.Div('Mois ref.'),
                           dcc.Dropdown(
                               id='which-month',
                               options=[{'label': dico[i], 'value': i} for i in range(1, 13)],
                               value=1,
                               disabled=True,
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
                html.Div([ html.Div('Jour ref.'),
                           dcc.Dropdown(
                               id='which-day',
                               options=[{'label': i, 'value': i} for i in range(1, 31)],
                               value=1,
                               disabled=True,
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Échelle de temps'),
                           dcc.RadioItems(
                               id='time-type',
                               options=[{'label':'Jour', 'value':'day'}, 
                                        {'label':'Mois','value':'month'},
                                        {'label':'Tous les mois', 'value':'year'}, 
                                        {'label':"A l'année",'value':'absolute'},
                                        {'label':'Tous les jours', 'value':'all'}],
                               value='all',
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                dcc.Markdown("""Le """)
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
                    [ dash.dependencies.Input('status-type', 'value'),
                      dash.dependencies.Input('time-type', 'value'),
                      dash.dependencies.Input('which-month', 'value'),
                      dash.dependencies.Input('which-day', 'value')])(self.makeMap)
        self.app.callback(
                    [ dash.dependencies.Output('which-month', 'disabled'),
                      dash.dependencies.Output('which-day', 'disabled')],
                      dash.dependencies.Input('time-type', 'value') )(self.disable_month_year)

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
                
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='CANCELLED_RATIO',
                                    labels={'CANCELLED_RATIO':'Pourcentage de vols annulés'}, hover_name='STATE_NAME',
                                    hover_data={'STATE_NAME': False}, color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état le " + str(day) + ' ' + self.dico[month] + ' 2019')
            else:
                data_delay = data_delay[(data_delay['MONTH'] == month) & (data_delay['DAY_OF_MONTH'] == day)]
                
                data_delay = data_delay.groupby(['STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='DELAY_MEAN',
                                    labels={'DELAY_MEAN':'Retard moyen'}, hover_name='STATE_NAME', hover_data={'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état le " + str(day) + ' ' + self.dico[month] + ' 2019')
        
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
                
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='CANCELLED_RATIO',
                                    animation_frame='DAY_OF_MONTH', labels={'CANCELLED_RATIO':'Pourcentage de vols annulés', 'DAY_OF_MONTH': 'jour'},
                                    hover_name='STATE_NAME', hover_data={'DAY_OF_MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'], title="Pourcentage de vols annulés par état en " + self.dico[month] + ' 2019')
            else:
                data_delay = data_delay[data_delay['MONTH'] == month]
                
                data_delay = data_delay.groupby(['DAY_OF_MONTH', 'STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='DELAY_MEAN',
                                    animation_frame='DAY_OF_MONTH', labels={'DELAY_MEAN':'Retard moyen', 'DAY_OF_MONTH': 'jour'},
                                    hover_name='STATE_NAME', hover_data={'DAY_OF_MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'], title="Retard moyen des vols par état en " + self.dico[month] + ' 2019')
        
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
                
                #data_cancel["MONTH"] = data_cancel["MONTH"].map(lambda x :self.dico["MONTH"][x])
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='CANCELLED_RATIO',
                                    animation_frame='MONTH', labels={'CANCELLED_RATIO':'Pourcentage de vols annulés', 'MONTH': 'mois'},
                                    hover_name='STATE_NAME', hover_data={'MONTH': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'], title="Pourcentage de vols annulés par état et par mois en 2019")
            else:
                data_delay = data_delay.groupby(['MONTH', 'STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                #data_delay["MONTH"] = data_delay["MONTH"].map(lambda x :self.dico["MONTH"][x])
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='DELAY_MEAN',
                                    animation_frame='MONTH', labels={'DELAY_MEAN':'Retard moyen', 'MONTH': 'mois'}, hover_name='STATE_NAME',
                                    hover_data={'MONTH': False, 'STATE_NAME': False}, color_continuous_scale=['white', 'blue'],
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
                
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='CANCELLED_RATIO',
                                    labels={'CANCELLED_RATIO':'Pourcentage de vols annulés'}, hover_name='STATE_NAME',
                                    hover_data={'STATE_NAME': False}, color_continuous_scale=['white', 'blue'],
                                    title="Pourcentage de vols annulés par état en 2019")
            else:
                data_delay = data_delay.groupby(['STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='DELAY_MEAN',
                                    labels={'DELAY_MEAN':'Retard moyen'}, hover_name='STATE_NAME', hover_data={'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'], title="Retard moyen des vols par état en 2019")
                
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
                fig = px.choropleth(data_cancel, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='CANCELLED_RATIO',
                                    animation_frame='DATE', labels={'CANCELLED_RATIO':'Pourcentage de vols annulés'},
                                    hover_name='STATE_NAME', hover_data={'DATE': False, 'STATE_NAME': False},
                                    color_continuous_scale=['white', 'blue'], title="Pourcentage de vols annulés par état et par jour en 2019")
            else:
                data_delay = data_delay.groupby(['DATE', 'STATE_NAME']).agg({'DEP_DELAY_NEW': ['mean']})
                data_delay.columns = ['DELAY_MEAN']
                data_delay = data_delay.reset_index()
                fig = px.choropleth(data_delay, locations='STATE_NAME', locationmode='USA-states', scope='usa', color='DELAY_MEAN',
                                    animation_frame='DATE', labels={'DELAY_MEAN':'Retard moyen'}, hover_name='STATE_NAME',
                                    hover_data={'DATE': False, 'STATE_NAME': False}, color_continuous_scale=['white', 'blue'],
                                    title="Retard moyen des vols par état et par jour en 2019")
        
        return fig

    def disable_month_year(self, type_jour):
        if type_jour == 'day':
            return False, False
        elif type_jour == 'month':
            return False, True
        else:
            return True,True
        
if __name__ == '__main__':
    nrg = Delay()
    nrg.app.run_server(debug=True, port=80)
