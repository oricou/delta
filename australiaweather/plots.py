from get_data import *


################Traitement des donnés et créations des DFs#################

def importStationDf(path='data/stations.csv'):
    '''
    Importe le dataset qui liste toutes les stations météos qui ont existé 
    en australie 
    '''
    return pd.read_csv(path,na_values=['-999.9'])

def csvToPickle(path='data/year_reports/'):
    '''
    lit et tranforme un fichier csv en format pickle
    '''
    if os.path.isfile(path): # re
        name, extension = os.path.splitext(path)
        pd.read_csv(path).to_pickle(name + '.pkl')
    if os.path.isdir(path):
        for filename in os.listdir(path):
            name, extension = os.path.splitext(filename)
            pd.read_csv(os.path.join(path, filename)).reset_index(drop = False).to_pickle(os.path.join(path, name) +'.pkl')





def stationLifeSpan(path='data/stations_mesures.csv'):
    """
    Crée le dataframe contenant l'année de mise en service et d'arret des stations
    """
    df = pd.read_csv('data/stations_mesures.csv', sep=' ', names=['ID', 'lat','long','info','from','to'])
    df = df.drop(columns=['lat','long','info'])
    df = df.groupby('ID', as_index =False).agg({'from' : 'min', 'to' : 'max'})#.sort_values(by=['from','to'], ascending=True)
    df.to_pickle('data/stations_lifespan.pkl')


def dataInventory():
    '''
    Construit un dataframe qui fait l'inventaire du nombre mesures en fonction 
    des stations météos et des années
    '''
    inventory = (pd.read_csv('data/stations_mesures.csv', sep = ' '
                ,names = ['ID', 'lat', 'long', 'info', 'from', 'to']
                ,usecols=['ID', 'lat', 'long', 'info', 'from', 'to']))

    num_df = (pd.DataFrame({'year':list(range(
                                        min(inventory['from']), 
                                        max(inventory['to'])))})) #liste les annés entre les permières et les dernières mesures
    num_df['number'] = 0 #initialise le nombre total de mesures
    num_df[inventory['info'].unique()] = 0 #Crée un colone pour chaque type de mesure
    for  index, r in inventory.iterrows():
        num_df.loc[(num_df["year"] >= r['from']) & (num_df["year"] <= r['to']), r['info']] += 1
        #^^ Sélectionne les annés tu df entre 'from' et 'to' puis incrépente la mesure 'info'
        num_df.loc[(num_df["year"] >= r['from']) & (num_df["year"] <= r['to']), 'number'] += 1
        #idem mais avec la colone number
    num_df.to_pickle('data/data_inventory.pkl')


def fromInventorySelect(start_year, end_year, info='PRCP'):
    '''
    Selectionne les stations qui ont enregristré des donnés du type séléctionné
    entre 'start year et end_year'
    '''
    inventory = pd.read_csv('data/stations_mesures.csv', sep =' ',names = ['ID', 'lat', 'long', 'info', 'from', 'to'], usecols=['ID', 'lat', 'long', 'info', 'from', 'to'] )
    inventory = inventory[inventory['info'] == 'PRCP']
    x = inventory.loc[((inventory["from"] <= start_year) & (inventory["to"] >= end_year)),]
    return x


def saveByYear(range_df,start,end ,path = 'data/year_reports'):
    '''
    Sauvegarde par ans sur la période 'start', 'end' le df rangedf
    range df est sous la forme :
    date (=mois de la mesure) | ID (de la station) | latitude | longitude | valeur de la mesure 
    '''
    dates = pd.to_datetime(range_df['date'], format='%Y-%m') # convertie les dates en format datetime pour une comparaison future
    range_df.reset_index(drop=True, inplace=True) # supprime l'index pour ne pas le sauvegarder dans le fichier

    for y in range(start, end+1): #parcours les annés 

        range_df.loc[dates.dt.year == y, ['date', 'ID', 'lat', 'long','value']].reset_index(drop=True).to_pickle(os.path.join(path,str(y)) + '.pkl')
        #^^ selectionnes les entrés correpondant à l'année, puis les sauvegarde sous forme pkl

def intervalNeeded(start, end, path = 'data/year_reports'):
    '''
    Determine les intervals non couvert par notre sauvegarde par année (cf saveByYear)
    Par exemple si l'on demande l'interval 1900 - 2000 et que [1950,1951,1980,1981] sont présents dans la sauvegarde,
    La fonctione renvera les intervals [(1900,1949),(1952,1979),(1982,2000)]
    '''
    existing = []
    missing = []
    for filename in os.listdir(path):
        year = int(filename[0:4])
        if year >= start and year <= end:
            existing.append(year) #filtre les annés déja existantes
                
    i = start
    while i < end :       
        while i in existing:
            i += 1
        if not i < end:
            break
        y = i
        while y not in existing and y < end:
            y += 1
        missing.append((i,y))
        i = y
    return missing,existing


def loadExisting(files,  path = 'data/year_reports/'):
    '''
    Loads the file, if the measures of the year have already been gathered and save localy
    '''
    dfs = []
    for f in files:
        print('loading', f)
        dfs.append(pd.read_pickle(path + str(f) + '.pkl')) #-------------------------------------change to load pickle
    return dfs

def readStationFile(ID, lat, lon, start_date, end_date):
        '''
        Construit un df depuis un fichier csv local, si celui ci n'est pas 
        disponible, il est téléchargé. 
        Le fichier csv a la forme :
        'ID' | 'date' | 'info' | 'value' 

        ID : l'id de la station 
        lat : latitude de la station (utilisé sur pour afficher les donnés plus tard)
        lon : longitude de la station (used for plotting later)
        start_date, end_date : the lifetime of the station we are interessted in
        '''
        dateparse = lambda x: datetime.strptime(x, '%Y%m%d')

        f = os.path.join('data','daily_stations', ID + '.csv')
        if not os.path.isfile(f): # re
            downloadSingleFile(ID)
        
        # Lit le fichier correspondant à la station
        tmp = (pd.read_csv(f,usecols = ['ID','date','info','value'],
                           date_parser = dateparse,parse_dates=['date'],
                          names = ['ID','date','info','value']))
        
        #filtre les entrés qui correspondent à la période voulue 
        #ainsi que l'information nécessaire (precipitations)
        tmp = (tmp.loc[(tmp['info'] == 'PRCP') 
                       & (tmp['date']>=start_date) 
                       & (tmp['date']<=end_date)])

        tmp.drop(['info'], inplace = True, axis =1) #nous ne gardons qu'un seul type d'info, préciser la nature de celle ci est inutile
        
        tmp['date'] = tmp['date'].dt.strftime('%Y-%m') #'arrondi la date au mois'
        tmp['lat'] = lat #mets à jour les coordonés de la stations (ils ne sont pas présents dans le csv)
        tmp['long'] = lon

        '''
        tmp = tmp.set_index('date')
        tmp = (tmp.resample('M').mean())#.ffill(1).reindex(time_range))
        tmp = tmp.reset_index('date')
        '''
        return tmp


def creationDfProcessPool(stations_id_df, start_year, end_year,path = 'data/daily_stations'):
    '''
    Crée le pool de process pour pour lire et rassembler les donnés des différents fichiers de stations.
    '''
    df = pd.DataFrame()
    needed = stations_id_df.shape[0]
    dateparse = lambda x: datetime.strptime(x, '%Y%m%d')

    start_date = dateparse(str(start_year)+'0101').strftime('%Y-%m')
    end_date = dateparse(str(end_year)+'1231').strftime('%Y-%m')

        
    #Construit la liste des paramètres pour les différents fichiers csv à lire afin de construire le dataset
    files = []
    for index, i in stations_id_df.iterrows():
        files.append((i['ID'], i['lat'], i['long'], start_date, end_date))
        
    with Pool(5) as pool: #crée une pool de process
        L = pool.starmap(func=readStationFile,iterable=files) #lit les différents fichiers et regroupe les dfs crées sous forme de liste
    # ^^ Pour la masse de donnée énorme à trier et mettre au bon format c'est très efficace (facteur 10)
    
    #df = pd.concat(L) la concaténation est plus efficace si elle n'est faite qu'une fois

    return L


def createEvolutionDataFrameOpti(start, finish):
    '''
    Crée le dataframe finale grace aux dataframes de toutes les stations étudiés.
    '''
    needed, existing = intervalNeeded(start, finish) #
    dfs = []

    for st,nd in needed:
        s = fromInventorySelect(st, nd) #selectionne les stations qui ont des mesures sur cet interval
        dfs.extend(creationDfToMapEvoOpti(s,st,nd)) #crée les dataframes pour les périodes non sauvegardés

    dfs.extend(loadExisting(existing)) #Charge sous forme de df les années déja calculés
    df = pd.concat(dfs) #rassemble le tout
    df = df.reset_index(drop=True)
    df = (df.groupby(['date', 'ID', 'lat', 'long'], as_index = False )['value']
            .sum() #somme toutes les mesures de précipitaions du même mois (les dates de mesures ont été arrondies au mois dans la fct readStationFile)
            .sort_values(by='date'))

    #saveByYear(df,start, finish) #sauvegarde les annés du df calculé afin de ne pas avoir à les recalculer la prochaine fois
    df.to_pickle('data/mesures_by_stations.csv')





def createPriceDf():
    '''
    Create the price df from the transaction files
    '''
    dateparse = lambda x: datetime.strptime(x, '%d-%m-%Y')
    df = pd.read_csv('data/Allocation_Trades.csv', low_memory=False, date_parser = dateparse,parse_dates=['date_of_approval'])
    df = df.drop(['qld_origin_trading_zone','qld_destination_trading_zone', 'regulated_unregulated', 'drainage_division' ,'murray_darling_basin_region'], axis = 1)
    #df = df.loc[((df['net_price'] != 0) & (df['dest_state'] !='Queensland')) ]
    df['date_of_approval'] = df['date_of_approval'].dt.strftime('%Y-%m')
    df = df.groupby(['date_of_approval','dest_state'], as_index=False)['price_per_ML'].mean() #effectue la moyenne sur le mois
    
    df = df.pivot(index='date_of_approval', columns='dest_state', values = 'price_per_ML').interpolate() #pivote le df pour mettre les sous indexes en colonnes pour pouvoir combles les donnés manquantes
    
    df = df.stack().to_frame('price_per_ML').reset_index(drop=False) # remets le dataframe dans sa configuration initiale et renomme la colone price_per_ML
    #df = df.reset_index(drop = False)

    df.to_pickle('data/prices.pkl')


################### Plots ############################

def plotStationLifeSpan(df, num_stations):
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

def plotEvolutionMap(mesures):
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


def plotPrices( price_df=createPriceDf(), geo_json='data/geo_datas/states.geojson'):
    '''
    Plots the territories' water price evoluting by month
    '''
    fig = px.choropleth(price_df,
                geojson=geo_json,
                locations='dest_state',
                featureidkey="properties.STATE_NAME",
                color="price_per_ML",
                animation_frame='date_of_approval',
                projection="mercator")

    #fig.update_geos(fitbounds="locations", visible=True)

    fig.show()

def main():
    stationLifeSpan()
    dataInventory()
    createEvolutionDataFrameOpti(2008,2021)
    createPriceDf()


    stations_lifespan = pd.read_pickle('data/stations_lifespan.pkl')

    data_inventory = pd.read_pickle('data/data_inventory.pkl')

    mesures_by_stations = pd.read_pickle('data/mesures_by_stations.csv')

    prices = pd.read_pickle('data/prices.pkl')

main()
