import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objs as go
from dash import dcc
from dash import html
from pandas import DataFrame
from plotly.subplots import make_subplots


def draw_globe_graph(countries, lst: list, emission: bool):
    if emission:
        data = [
            dict(type='choropleth', locations=countries, z=lst, locationmode='country names', text=countries,
                 marker=dict(line=dict(color='rgb(0,0,0)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='Mean\nEmission,\n(MtCO₂e)'))]
        layout = dict(title='Mean CO2 emission in countries (1990 - 2018)',
                      geo=dict(showframe=False, showocean=True, oceancolor='rgb(0,255,255)',
                               projection=dict(type='orthographic', rotation=dict(lon=60, lat=10), ),
                               lonaxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)'),
                               lataxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)')), )
        return dict(data=data, layout=layout)
    else:
        data = [
            dict(type='choropleth', locations=countries, z=lst, locationmode='country names', text=countries,
                 marker=dict(line=dict(color='rgb(0,0,0)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='# Temperature\nDifferences,\n°C'))]
        layout = dict(title='Temperature differences in countries (1900 - 2013)',
                      geo=dict(showframe=False, showocean=True, oceancolor='rgb(0,255,255)',
                               projection=dict(type='orthographic', rotation=dict(lon=60, lat=10), ),
                               lonaxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)'),
                               lataxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)')), )
        return dict(data=data, layout=layout)


def get_temp_diff(df: DataFrame):
    countries = np.unique(df[df['Country'] != 'World']['Country'])
    temp_dif_lst = []
    for country in countries:
        country_temp = df[(df['Country'] == country) & (
                (df['Year'] == 2013) | (df['Year'] == 1900))][
            'AverageTemperature'].diff()
        country_temp.drop(index=country_temp.index[0], axis=0,
                          inplace=True)
        temp_dif_country = country_temp.values
        if len(temp_dif_country) > 0:
            temp_dif_lst.append(temp_dif_country[0])
    return countries, temp_dif_lst


def get_mean_emission(df: DataFrame):
    countries_emission = np.unique(df[df['Country'] != 'World']['Country'])
    mean_emission_lst = []
    for country in countries_emission:
        mean_total_emission = df[(df['Country'] == country)]['Mean']
        if len(mean_total_emission.values) > 0:
            mean_emission_lst.append(mean_total_emission.values[0])
    return countries_emission, mean_emission_lst


def load_cleaned_dataframe_from_csv(filename: str, cols: int):
    return pd.read_csv(filename, usecols=[i for i in range(1, cols)])


class GlobalWarming:

    def __init__(self, application=None):
        clean_temp_df = load_cleaned_dataframe_from_csv(
            "phllhlv_emissionglobalwarming/data/clean/clean_global_land_temperature_by_country.csv", cols=4)
        clean_emission_df = load_cleaned_dataframe_from_csv(
            "phllhlv_emissionglobalwarming/data/clean/clean_total_emission_by_country.csv", cols=4)
        clean_mean_emission_df = load_cleaned_dataframe_from_csv("phllhlv_emissionglobalwarming/data/clean"
                                                                 "/clean_mean_emission_by_country.csv",
                                                                 cols=36)
        clean_temp_df.dropna(inplace=True)
        clean_emission_df.dropna(inplace=True)

        self.clean_emission_df = clean_emission_df.copy()
        self.clean_temp_df = clean_temp_df.copy()

        # Drawing globe graph
        countries, temp_def_lst = get_temp_diff(clean_temp_df)
        fig_temp = draw_globe_graph(countries, temp_def_lst, False)

        countries_emission, mean_emission_lst = get_mean_emission(clean_mean_emission_df.iloc[1:, :])
        fig_emission = draw_globe_graph(countries_emission, mean_emission_lst, True)

        fig_line_us = self.draw_line_graph("United States")

        self.countries = np.unique(clean_temp_df.Country)
        self.main_layout = html.Div(children=[
            html.H3(children="Analysis of the state of global warming in each country in regard to its total CO2 "
                             "emission from the industrial sectors"),
            html.Div(children=[html.Div([dcc.Graph(figure=fig_temp), ], style={'width': '100%', }),
                               html.Br(),
                               html.Div([dcc.Graph(figure=fig_emission), ], style={'width': '100%', }),
                               html.Br()], style={
                'display': 'flex'
            }),
            dcc.Markdown("""
            * Commentary (Orthographic Graph):
                * The globes are interactive, you can see the values in each country by 
                hovering the mouse over the location of the country on the globe. This helps the user to have a bird's-eye
                view over certain geographically regions and the effect of global warming on such regions.
                * The two globes indicate the temperature differences from 1900 to 2013 and the total CO2 emission 
                from 1990 to 2018 in each country. 
                * For the temperature differences globe, we took the difference between the average temperature of the
                year 1990 and the average temperature of the year 2013. As we can see from the globe, countries such as: 
                China, the United States, India, Japan, Canada, Mexico... have the biggest temperature difference.
                * For the total C02 emission globe, we used the mean value of the yearly total CO2 emission 
                from 1990 to 2018. As we can see on this globe, the countries that have the highest total CO2 emission 
                are: China, the United States, India, Japan...
                * From the two globes, we can see that the countries that have highest total CO2 emission are also 
                the ones that have the biggest temperature differences. Therefore, the CO2 emission affects 
                on the warming in each countries.
            """),
            html.Div([html.Div('Countries'),
                      dcc.Dropdown(
                          id='glb-which-countries',
                          options=[{'label': country, 'value': country} for country in self.countries],
                          value='World',
                      ),
                      ], style={'width': '25%', 'padding': '2em 0px 0px 0px'}),
            html.Div([dcc.Graph(figure=fig_line_us, id='glb-line-graph'), ], style={'width': '100%', }),
            dcc.Markdown("""
            * Commentary (Line Graph):
                * The graph represents the trend between the difference in average temperature and in total emission of 
                a country on a given period of time
                * The default value of the filter is World
                    * Provide a generalized view of the correlation between global warming and annual global total 
                    emission
                * The resulting trend can be monitor more closely with the filter being switched to a specific country.
                For example, China has an exponential increase in total CO2 emission around the year 2000 when they 
                went into industrialization. A decade later around the year 2012, a massive spike on their average temperature
                was recorded by almost 1.5 degree Celsius compare to half a decade before. As the total CO2 emission 
                increases over the years, the average temperature experiences the same trend.
                * The similar trend in China can be seen in many other big industrial countries 
                such as: the United States, India, Japan... and ultimately the world. We can see that over the years, 
                the global average temperature increases as the total CO2 emission of the world rises.
                * Limited access to data is a draw back of this project since the availability of emission data only 
                dates back from 1990
            ### Credits:
            * Sources : 
               * [Climate change:](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data) Earth Surface Temperature Data
               * [Climate Watch:](https://www.climatewatchdata.org/data-explorer/historical-emissions?historical-emissions-data-sources=cait&historical-emissions-gases=All%20Selected%2Cco2&historical-emissions-regions=All%20Selected&historical-emissions-sectors=All%20Selected&page=1) Historical Emission
            * (c) 2022 Luu Hoang Long Vo, Phu Hien Le
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
            dash.dependencies.Output('glb-line-graph', 'figure'),
            [dash.dependencies.Input('glb-which-countries', 'value')]
        )(self.draw_line_graph)

    def draw_line_graph(self, country: str):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        country_temp = self.clean_temp_df[self.clean_temp_df.Country == country]
        country_emission = self.clean_emission_df[self.clean_emission_df.Country == country]

        fig.add_trace(go.Scatter(x=country_temp.Year, y=country_temp.AverageTemperature, name="Average Temperature (°C)"),
                      secondary_y=False)

        fig.add_trace(go.Scatter(x=country_emission.Year, y=country_emission.TotalEmission, name="Total Emission (MtCO₂e)"),
                      secondary_y=True)

        fig.update_layout(title_text="Average Temperature and Total Emission of " + country)
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Temperature", secondary_y=False)
        fig.update_yaxes(title_text="Total Emission", secondary_y=True)
        return fig


if __name__ == '__main__':
    nrg = GlobalWarming()
    nrg.app.run_server(debug=True, port=8051)
