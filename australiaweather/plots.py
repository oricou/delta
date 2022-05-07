from get_data import *

##Les plots suivant sont fait pour jupyter (d'où 'fig.show()')

def plotStationLifeSpan(df, num_stations=None): #from stationLifeSpan (pk pas faire une molette qui selectionne le nbr de stations à afficher )
    df_plot = df.copy() if num_stations == None else df.head(num_stations).copy()
    df_plot['timespan'] = df['to']-df['from']
    df_plot = df_plot.sort_values(by='timespan', ascending=True)
    fig = px.bar(df_plot, x='ID', y='timespan', base = 'from',  barmode = 'group',
                 labels = {'ID':'Stations','timespan':'Years of existence'}, title = "Stations' lifespans",
                 range_x=(0,df_plot.shape[0]),opacity=1) 
    fig.update_traces(marker_color='green')
    fig.update_xaxes(ticktext=[], tickvals=[])
    fig.update_layout(yaxis_range=[min(df_plot['from'])*0.99, max(df_plot['to']*1.01)])
    fig.update_xaxes(constrain='range')
    fig.update_traces(hovertemplate ='<b>ID</b>: %{x}'+'<br>from : %{base}'+'<br>to : %{y}')

    fig.show()

def plotMeasuresInventory(df): 
    fig = px.bar(df, x = 'year', y = df.columns[2:], title = "Number of measure depending the year")
    fig.show()

def plotEvolutionMap(mesures): #(from createEvolutionDataFrameOpti)
    '''
    Plots the map of all the stations and their precipitation evoluting by month

    '''
    fig = (px.scatter_mapbox(mesures, lat='lat', lon='long',
    hover_name="ID",
    animation_group="ID",
    animation_frame="date",
    color='value',
    range_color = [0,6000],
    zoom=3, height=500))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()


import json
import time

def plotPrices( price_df=createPriceDf(), geo_json='data/geo_datas/states.geojson'):
    '''
    Plots the territories' water price evoluting by month
    '''
    start = time.time()
    fig = (px.choropleth(price_df,
                geojson=geo_json,
                locations=price_df['dest_state'],
                featureidkey="properties.STATE_NAME",
                color="price_per_ML",
                animation_frame='date_of_approval',
                projection="mercator",
                range_color=[0,500]))

    fig.update_geos(fitbounds="locations", visible=True)
    end = time.time()
    print(end - start)

    fig.show()


def main():
    createEvolutionDataFrameOpti(1870, 1871)

main()