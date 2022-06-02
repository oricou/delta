import sys
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import html
from dash import dcc
import pycountry_convert as pc
import dash
# -*- coding: utf-8 -*-

pd.options.plotting.backend = "plotly"

# ========================================================================================
#
#
#                            DATA LOADING AND VARIABLE DECLARATIONS
#
#
# ========================================================================================

data = pd.read_csv(
    'data/YA_CDL_Energy_generation/energy_per_source.csv').drop(columns=['Unnamed: 0'])
energy_per_area = pd.read_csv(
    'data/YA_CDL_Energy_generation/energy_per_area.csv').drop(columns=['Unnamed: 0'])
data_per_year = {str(year):     data[data['Year'] == year]
                 for year in range(2000, 2021)}

areas = data['Area'].unique()

area_minus_europe = [
    countries for countries in areas if countries not in ['EU-27', 'EU27+1']]


columns = energy_per_area.columns.to_numpy()[2:]
dropdown_options = [{'label': columns[i], 'value': i}
                    for i in range(len(columns)) if '(log_10)' not in columns[i]]
(dropdown_options[0], dropdown_options[4]) = (
    dropdown_options[4], dropdown_options[0])
y_axis = {str(i): columns[i] for i in range(len(columns))}

fossil_energies = ['Fossil', 'Coal', 'Hard Coal',
                   'Lignite', 'Gas', 'Other fossil', 'Nuclear']
renewable_energies = ['Renewable', 'Hydro', 'Wind and solar',
                      'Wind', 'Solar', 'Bioenergy', 'Other renewables']
colorscales = {col: ('Greens' if any(map(
    (lambda energie: energie in col), renewable_energies)) else 'Reds') for col in columns}
colorscales['Total energy generation (TWh)'] = 'Blues'
colorscales['Total energy generation (TWh) (log_10)'] = 'Blues'


class EuropeEnergyGeneration():
    START = 'Start'
    STOP = 'Stop'

    def __init__(self, app = None):
        self.colorscales = colorscales
        self.dropdown_options = dropdown_options
        self.data_per_year = data_per_year
        self.energy_per_area = energy_per_area
        self.df = data
        self.years = [i for i in range(2000, 2021)]
        self.y_axis = y_axis
        self.is_autoslider_activated = False
        self.colors = {
            'thirdly': '#D3D3D3',
            'secondary': '#111111',
            'background': '#111111',
            'text': '#7FDBFF'
        }

        # ========================================================================================
        #
        #
        #                            APP LAYOUT
        #
        #
        # ========================================================================================

        self.main_layout = html.Div(children=[
            html.H1(children='Energy generation in the European Union from 2000 to 2020',
                    style={
                        'textAlign': 'center'
                    }),

            html.Div(children=[
                html.Div(
                    dcc.Dropdown(
                        dropdown_options,
                        value=4,
                        id='y-axis',
                        searchable=True,
                        style={
                            'backgroundColor': self.colors['thirdly'],
                            'color': self.colors['text']
                        }
                    ),
                    style={'width': '35%',
                           'display': 'inline flow-root',
                           }
                ),

                html.Div(
                    dcc.RadioItems(options=[
                        {'label': 'Linear', 'value': 0},
                        {'label': 'Log', 'value': 1}
                    ],
                        value=0,
                        id='scale',
                        style={
                        'display': 'flex'
                    }
                    ),
                    style={
                        'paddingLeft': '4%',
                        'width': '33%',
                        'display': 'flex',
                        'flexDirection': 'row',
                        'alignItems': 'center'
                    }
                )],
                style={
                'paddingLeft': '30%',
                'display': 'flex'
            }
            ),

            html.Div(children=[
                html.Div(children=[
                    html.Div(
                        dcc.Graph(id='country-sunburst',
                                  style={
                                      'display': 'inline-block'
                                  })
                    ),
                    html.Div(
                        dcc.Graph(
                            id='europe27+1-sunburst',
                            style={
                                'display': 'inline flow-root list-item'
                            })
                    ),
                ],
                    style={}
                ),
                html.Div(children=[
                    html.Div(
                        dcc.Graph(
                            id='Europe-Map',
                            style={
                                'width': '100%',
                                'height': '80%',
                                'display': 'inline-block'
                            }
                        ),
                        style={
                            'width': '100%',
                            'height': '100%',
                        }
                    ),
                    html.Div(
                        dcc.Graph(id='evolution-line-plot',
                                  style={
                                      'width': '100%',
                                      'height': '80%',
                                      'display': 'inline flow-root list-item'
                                  }),
                        style={
                        }
                    ),
                ])
            ],
                style={
                'backgroundColor': self.colors['secondary'],
                'color': self.colors['text'],
                'display':'flex',
                'alignItems':'center'
            }),

            html.Div(children=[
                html.Div(children=[
                    html.Button(
                        self.STOP,
                        id='button-start-stop',
                        style={'display': 'inline-block'}
                    ),
                    html.Div(
                        dcc.Slider(
                            id='crossfilter-year-slider',
                            min=self.years[0],
                            max=self.years[-1],
                            step=1,
                            value=2019,
                            marks={str(year): {'label': str(year),
                                   'style': {'color': self.colors['text'],
                                             'backgroundColor': self.colors['secondary']}}
                                   for year in self.years}
                        ),
                        style={'display': 'inline-block',
                               'width': "90%",
                               }
                    ),
                    dcc.Interval(            # fire a callback periodically
                        id='auto-stepper',
                        disabled=self.is_autoslider_activated,
                        interval=1000,       # in milliseconds
                        max_intervals=-1,  # start running
                        n_intervals=0
                    ),
                ],
                    style={
                    'display': 'flex'
                }),
                html.Div(children=[
                    html.H5("Click on a the cross next to a country to unselect it from the map/ select it from the dropdown",
                            style={
                                'textAlign': 'center'
                            }),
                    dcc.Dropdown(
                        area_minus_europe, area_minus_europe, multi=True, id='selected-areas-for-map',
                        style={
                            'backgroundColor': self.colors['secondary'],
                            'color': self.colors['text']
                        }
                    )],
                    style={
                        'display': 'flex',
                        'flexDirection': 'column'
                }
                ),
                dcc.Markdown("""
   #### About

   * [Plotly version](https://plotly.com/python/v3/gapminder-example/)
   * Data : [DataWorld, from data of Ember-Climate](https://data.world/makeovermonday/2021w5)
   * (c) 2022 Yacine Anane & Charli De Luca
   """),

            ])
        ],
            style={
            'backgroundColor': self.colors['background'],
            'color': self.colors['text']})

        if app:
            self.app = app
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


        # ========================================================================================
        #
        #
        #                            CALLBACKS
        #
        #
        # ========================================================================================
        self.app.callback(
            dash.dependencies.Output('Europe-Map', 'figure'),
            dash.dependencies.Input('crossfilter-year-slider', 'value'),
            dash.dependencies.Input('y-axis', 'value'),
            dash.dependencies.Input('selected-areas-for-map', 'value'),
            dash.dependencies.Input('scale', 'value')
        )(self.create_map)

        self.app.callback(
            dash.dependencies.Output('country-sunburst', 'figure'),
            dash.dependencies.Input('Europe-Map', 'clickData'),
            dash.dependencies.Input('crossfilter-year-slider', 'value')
        )(self.update_sunburst_country)

        self.app.callback(
            dash.dependencies.Output('europe27+1-sunburst', 'figure'),
            dash.dependencies.Input('crossfilter-year-slider', 'value')
        )(self.update_sunburst_europe)

        self.app.callback(
            dash.dependencies.Output('evolution-line-plot', 'figure'),
            dash.dependencies.Input('y-axis', 'value'),
            dash.dependencies.Input('scale', 'value')
        )(self.update_line_plot)

        self.app.callback(
            dash.dependencies.Output('crossfilter-year-slider', 'value'),
            dash.dependencies.Input('auto-stepper', 'n_intervals'),
            [dash.dependencies.State('crossfilter-year-slider', 'value'),
             dash.dependencies.State('button-start-stop', 'children')]
        )(self.on_interval)

        self.app.callback(
            dash.dependencies.Output('button-start-stop', 'children'),
            dash.dependencies.Input('button-start-stop', 'n_clicks'),
            dash.dependencies.State('button-start-stop', 'children')
        )(self.button_on_click)

        self.app.callback(
            dash.dependencies.Output('auto-stepper', 'max_interval'),
            [dash.dependencies.Input('button-start-stop', 'children')]
        )(self.run_movie)

        self.app.callback(
            dash.dependencies.Output('text-sunburst-country', 'children'),
            dash.dependencies.Input('Europe-Map', 'clickData')
        )(self.update_country_name)

    def create_map(self, year, y_axis_value, selected_areas, scale):
        world_data = self.energy_per_area[self.energy_per_area['Area'].isin(
            selected_areas)]

        world_data = world_data[world_data['Year'] == year]

        color_column = self.y_axis[str(y_axis_value)] if scale == 0 else (
            self.y_axis[str(y_axis_value)] + ' (log_10)')
        zmax = world_data[color_column].max()
        zmin = world_data[color_column].min()

        fig = go.Figure(data=go.Choropleth(
            locations=world_data['iso_alpha3'],
            z=world_data[color_column],
            text=world_data['Area'],
            colorscale=self.colorscales[color_column],
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title=color_column,

            zmax=zmax,
            zmin=zmin
        ))

        fig.update_geos(
            projection_scale=4.5,
            center={'lat': 52, 'lon': 11.977321}
        )

        fig.update_layout(
            title_x=0.5,

            width=1200,
            height=500,
            legend={
                "borderwidth": 0
            },

            plot_bgcolor=self.colors['secondary'],
            paper_bgcolor=self.colors['secondary'],
            font_color=self.colors['text'],

            title_text=self.y_axis[str(y_axis_value)] + ' in EU countries in ' + str(year) +
            "<br><sup>(Click a country to display a pie chart of it's energy generation distribution)</sup>",
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )
        return fig

    def update_line_plot(self, y_axis_value, scale):
        value_column = self.y_axis[str(y_axis_value)] if scale == 0 else (
            self.y_axis[str(y_axis_value)] + ' (log_10)')
        fig = px.line(self.energy_per_area, x="Year",
                      y=value_column, color='Area')

        fig.update_layout(
            title_text="Evolution of '" + value_column.lower() + "' in EU countries" +
            "<br><sup>(Double click on a country to isolate it's    data)</sup>",
            title_x=0.5,

            width=1200,
            height=300,
            plot_bgcolor=self.colors['secondary'],
            paper_bgcolor=self.colors['secondary'],
            font_color=self.colors['text']
        )

        return fig

    def update_sunburst_country(self, clickData, year):
        area = 'France' if clickData == None else clickData['points'][0]['text']
        unwanted_variables = ['Demand', 'Production',
                              'Net imports', 'Fossil', 'Renewables', 'Wind and solar']
        selected_data = self.df[(self.df['Year'] == year)
                                & (self.df['Area'] == area)]
        selected_data = selected_data[~selected_data['Variable'].isin(
            unwanted_variables)]

        fig = px.sunburst(selected_data, path=['Kind of energy', 'Variable'],
                          values='Generation (TWh)',
                          hover_name='Variable',
                          hover_data=['Generation (TWh)'],
                          width=450, height=400,
                          color_discrete_map={
            'Nuclear': 'gold', 'Renewables': '#32CD32'}
        )

        fig.update_layout(
            title_text='Energy generation in ' + area + ' ' + 'in ' + str(year) +
            "<br><sup>(Click another country on the map to display it's energy generation distribution)</sup>",
            title_x=0.5,
            plot_bgcolor=self.colors['secondary'],
            paper_bgcolor=self.colors['secondary'],
            font_color=self.colors['text']
        )

        return fig

    def update_sunburst_europe(self, year):
        area = 'EU27+1'
        unwanted_variables = ['Demand', 'Production',
                              'Net imports', 'Fossil', 'Renewables', 'Wind and solar']
        selected_data = self.df[(self.df['Year'] == year)
                                & (self.df['Area'] == area)]
        selected_data = selected_data[~selected_data['Variable'].isin(
            unwanted_variables)]
        fig = px.sunburst(selected_data, path=['Kind of energy', 'Variable'],
                          values='Generation (TWh)',
                          hover_name='Variable',
                          hover_data=['Generation (TWh)'],
                          title='Energy generation in EU in ' + str(year),
                          width=450, height=400,
                          color_discrete_map={
            'Fossil': 'gold', 'Renewables': '#32CD32'}
        )

        fig.update_layout(
            title_x=0.5,
            plot_bgcolor=self.colors['secondary'],
            paper_bgcolor=self.colors['secondary'],
            font_color=self.colors['text']
        )
        return fig

    def run_movie(self, text):
        if text == self.START:
            return 0
        else:
            return -1

        # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            self.is_autoslider_activated = False
            return self.STOP
        else:
            self.is_autoslider_activated = True
            return self.START

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year  # nothing changes

    def update_country_name(self, clickData):
        input_value = 'France' if clickData == None else clickData['points'][0]['text']
        return f"Distribution of Energy Type in {input_value}"

    def run(self, host = "0.0.0.0", debug = False, port = 8050):
        if host == "0.0.0.0":
            self.app.run_server(host="0.0.0.0", debug=debug, port=port)
        else:
            self.app.run_server(host = host, debug = debug)
        self.update_sunburst_country(None, 2020)
        self.update_sunburst_europe(2020)
        self.update_line_plot(0)
        self.create_map(2000, 4)


if __name__ == '__main__':
    eeg = EuropeEnergyGeneration()
    if len(sys.argv) > 1:
        eeg.run(host = sys.argv[1], debug=False)
    else:
        eeg.run(host="0.0.0.0", debug=False)
