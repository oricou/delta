import sys
import dash
import flask
from dash import dcc
from dash import html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class DeathAnalysis():
    START = 'Start'
    STOP  = 'Stop'
    
    def __init__(self, application = None):
        #open Data
        frame = pd.read_csv("hcbjbd_Deces_dans_le_monde_classe_par_cause/data/data.csv", sep=";")
        #Create Frame
	    #New Start
        frame = frame.fillna(0)

        self.select_columns = ['Méningite', 'Cancer', 'Feu, chaleur et substances brulante'
                         , 'Malaria', 'Noyade', 'Aggression physique', 'SIDA', 'Overdose médicamenteuse'
                        , 'Tuberculose', 'Accident routier', 'Trouble maternel', 'Infection respiratoire'
                        , 'Désordre Néonatal', 'Alcoolisme', 'Forces de la nature'
                        , 'Maladie diarrhéique', 'Exposition à la chaleur et au froid environmentale', 'Déficite nutritionnel'
                        , 'Auto infligé', 'Conflit et terrorisme', 'Diabetes', 'Empoisonement', 'Malnutrition', 'Terrorisme', 'Maladie cardiovasculaire'
                        , 'maladie rénale chronique', 'maladie réspiratoire chronique', 'Cirrhose et autre maladie chronique du foie', 'Maladie digestive', 'Hépatite aiguë'
                        , 'Alzheimer et autre démences', 'maladie de Parkinson'] 

        self.mask_year = frame[(frame['Year']==2007)]
        self.mask_country = frame['Country'] == 'France'
        
        
        number_of_countries = ['Pays le plus touché', 'Les 3 pays les plus touchés', 'Les 5 pays les plus touchés', 'Les 10 pays les plus touchés', 'Les 20 pays les plus touchés']

        #Extract Series
        country = frame['Country']
        countries = list(dict.fromkeys(country))
        year = frame['Year']
        years = list(dict.fromkeys(year))
        code = frame['Code']

        self.dict_of_countries = {'Pays le plus touché': 1, 'Les 3 pays les plus touchés': 3, 'Les 5 pays les plus touchés': 5, 'Les 10 pays les plus touchés': 10, 'Les 20 pays les plus touchés': 20}




        #Compute percentage
        res = frame[self.select_columns].div(frame[self.select_columns].sum(axis=1), axis=0)*100
        res.insert(loc=0, column='Country', value=country)
        res.insert(loc=1, column="Year", value=year)
        res.insert(loc=1, column='Code', value=code)
        self.res = res
        self.years = sorted(set(self.res["Year"]))

        #New End
        self.frame = frame
        self.main_layout = html.Div(children=[
        
        html.H3(children='Pourcentage des causes de mortalité par pays'),
        html.Div([  dcc.Dropdown(self.select_columns, 'Cancer', placeholder='Select causes..', id='causes-dropdown')]),
        html.Div([  dcc.Graph(id='da-choropleth-graph', style={'width':'100%'})]),
        
        html.Button(self.START, id='da-button-start-stop', style={'display':'inline-block'}),
        

        html.Div([
            html.Div(
                dcc.Slider(
                        id='da-crossfilter-year-slider',
                        min=self.years[0],
                        max=self.years[-1],
                        step = 1,
                        value=self.years[0],
                        marks={str(year): str(year) for year in self.years[::3]},
                ),
                style={'display':'inline-block', 'width':"90%"}
            ),
            dcc.Interval(
                id='da-auto-stepper',
                interval=1000,
                max_intervals = -1,
                n_intervals = 0
            ),
            ], style={
                'padding': '0px 50px', 
                'width':'100%'
            }),

        html.Div([
        html.H3(children='Répartition du nombre de décès'                             ,   style={'display':'inline-block'}),
        html.H3(children='Evolution de la cause de mortalité.',   style={'display':'inline-block', 'padding-left' : '30%'}),
        ]),
        html.Div([
            dcc.Graph(id='da-sunburst-graph',
                style={'width':'49%', 'display':'inline-block'}),
            dcc.Graph(id='da-scatter-graph',
                style={'width':'49%', 'display':'inline-block', 'padding-left': '0.5%'}),  
        ]),

        html.Div([  dcc.Dropdown( number_of_countries, 'Les 10 pays les plus touchés',placeholder='Select top countries...', id='countries-dropdown')]),
        
        html.Br(),
        dcc.Markdown("""
        #### Information Générale

        La carte du monde intéractive permet de nous montrer avec précision l'impact et l'évolution de la cause de mortalité étudié à travers le temps.
        On observe une disparité entre les pays développés et les pays en voie de développement.

        Le graphique en camembert indique le positionnement des pays vis-à-vis de la cause

        Le graphique en nuage de point indique l'évolution de la cause sur les trentes dernières années.

        Comme exemple, nous pouvons citer la hausse du cancer au Canada (En %) et de la diminution de la malaria en Inde (En %) (Visible sur la carte intéractive).
        #### À propos

        * Données : https://ourworldindata.org/causes-of-death

        * (c) 2022 Jean-Baptiste DELOGES Hugo CANTON-BACARA
        """),
        ]),
        
  
        html.Br(),


        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        self.app.callback(
                    dash.dependencies.Output('da-sunburst-graph', 'figure'),
                    [dash.dependencies.Input('countries-dropdown', 'value'),
                    dash.dependencies.Input('da-crossfilter-year-slider', 'value'),
                    dash.dependencies.Input('causes-dropdown', 'value')])(self.update_sunburst_graph)
        self.app.callback(
                    dash.dependencies.Output('da-scatter-graph', 'figure'),
                    [dash.dependencies.Input('countries-dropdown', 'value'),
                    dash.dependencies.Input('causes-dropdown', 'value')])(self.update_scatter_graph)
        self.app.callback(
                    dash.dependencies.Output('da-choropleth-graph', 'figure'),
                    [dash.dependencies.Input('causes-dropdown', 'value'),
                    dash.dependencies.Input('da-crossfilter-year-slider', 'value')])(self.update_choropleth_graph)

        self.app.callback(
                    dash.dependencies.Output('da-button-start-stop', 'children'),
                    dash.dependencies.Input('da-button-start-stop', 'n_clicks'),
                    dash.dependencies.State('da-button-start-stop', 'children'))(self.button_on_click) 

        self.app.callback(
            dash.dependencies.Output('da-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('da-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('da-crossfilter-year-slider', 'value'),
             dash.dependencies.State('da-button-start-stop', 'children')])(self.on_interval)

    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START
    
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year

    def update_choropleth_graph(self, cause_value, year_value):
        mask_year = self.frame['Year']==int(year_value)
        fig = px.choropleth(self.res[mask_year], locations="Code",
                    color=str(cause_value),
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    width=1500,
                    height=500)
        return fig

    def update_sunburst_graph(self, country_value, year_value, cause_value):
        mask_year = self.frame[(self.frame['Year']==int(year_value))]
        mask_cause = mask_year.sort_values(str(cause_value), ascending=False)
        mask_cause = mask_cause.head(self.dict_of_countries[str(country_value)])
        mask_cause = mask_cause[mask_cause[str(cause_value)]!=0]
        fig = px.sunburst(mask_cause, path=['Country'], values=str(cause_value), 
        color=str(cause_value), hover_data=['Code'])
        return fig

    def mask_countries(self, countries, nb, index):
        if nb == 1 :
            mask_country = ((self.frame['Country']==countries[index[0]]))
        elif nb == 3 :
            mask_country = ((self.frame['Country']==countries[index[0]]) | (self.frame['Country']==countries[index[1]]) | (self.frame['Country']==countries[index[2]]))
        elif nb == 5 :
            mask_country = ((self.frame['Country']==countries[index[0]]) | (self.frame['Country']==countries[index[1]]) | (self.frame['Country']==countries[index[2]]) | (self.frame['Country']==countries[index[3]]) |
                (self.frame['Country']==countries[index[4]]))
        elif nb == 10 :
            mask_country = ((self.frame['Country']==countries[index[0]]) | (self.frame['Country']==countries[index[1]]) | (self.frame['Country']==countries[index[2]]) | (self.frame['Country']==countries[index[3]]) |
                (self.frame['Country']==countries[index[4]]) | (self.frame['Country']==countries[index[5]]) | (self.frame['Country']==countries[index[6]]) |
                (self.frame['Country']==countries[index[7]]) | (self.frame['Country']==countries[index[8]]) | (self.frame['Country']==countries[index[9]]))
        elif nb == 20 :    
            mask_country = ((self.frame['Country']==countries[index[0]]) | (self.frame['Country']==countries[index[1]]) | (self.frame['Country']==countries[index[2]]) | (self.frame['Country']==countries[index[3]]) |
                (self.frame['Country']==countries[index[4]]) | (self.frame['Country']==countries[index[5]]) | (self.frame['Country']==countries[index[6]]) |
                (self.frame['Country']==countries[index[7]]) | (self.frame['Country']==countries[index[8]]) | (self.frame['Country']==countries[index[9]]) | (self.frame['Country']==countries[index[10]]) | (self.frame['Country']==countries[index[11]]) | (self.frame['Country']==countries[index[12]]) | (self.frame['Country']==countries[index[13]]) |
                (self.frame['Country']==countries[index[14]]) | (self.frame['Country']==countries[index[15]]) | (self.frame['Country']==countries[index[16]]) |
                (self.frame['Country']==countries[index[17]]) | (self.frame['Country']==countries[index[18]]) | (self.frame['Country']==countries[index[19]]))
        return mask_country

    def update_scatter_graph(self, country_value, cause_value):
        frame_year = self.frame[(self.frame['Year']==2019)]
        frame_year = frame_year.sort_values(str(cause_value), ascending=False)
        nb_countries = self.dict_of_countries[str(country_value)]
        countries = frame_year.head(nb_countries)['Country']
        index = countries.index
        mask_country = self.mask_countries(countries, nb_countries, index)
        fig = px.scatter(self.frame[mask_country], x="Year", y=str(cause_value), color='Country')
        return fig


if __name__ == '__main__':
    da = DeathAnalysis()
    da.run(port=8055)
