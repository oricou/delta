# Ce fichier contient le texte des éléments HTML afin de ne pas encombrer le fichier principal

txt_title = 'Vaccinations contre le COVID-19 par pays en fonction du temps'

txt_p1 = '''
On va présenter ci-dessous les liens entre les taux de vaccinations contre le COVID-19 et le PIB par habitant.
Pour simplifier les résultats, nous ne garderons les données qu'à partir du 1er janvier 2021 (inclus). Les données
du PIB datent de 2016 car aucune donnée n'était disponible pour tous les pays au dela de cette année-là.
Source des données :
'''

txt_p2 = '''
Nous commençons par afficher l'évolution des taux de vaccination par pays en fonction du temps. Les paramètres
disponibles sont distinguables en 3 catégories : vaccinations quotidiennes, vaccinations pour 100 habitants et
vaccinations totales. On affiche donc les courbes sur 3 graphiques différents pour avoir des échelles plus adaptées.
'''

txt_p3 = '''
On constate donc un palier dans les vaccinations totales qui s'explique par le délais entre les 2 premières doses
et la mise en place de la 3e dose plus tard dans l'année. On remarque beaucoup de données manquantes pour les pays
qui, à première vue, semble avoir un développement assez limité. On voit également des "saut" dans les données,
notamment en Chine. Pour les vaccinations quotidiennes, on remarque une forte fluctuation due au weekend
(principalement le dimanche) car il y a peu voire pas de vaccination ces jour-ci dans de nombreux pays. Pour lisser
cette donnée, le jeu de données propose un paramètre "net" qui fait une moyenne sur 7 jours glissants.
'''

txt_p4 = '''
On affiche maintenant un graphique qui représente l'évolution du pourcentage de la population qui a reçu une
vaccination sur 5 continents. Les données sur l'Amérique du Sud présentaient trop de valeurs manquantes pour être
affichées.'''

txt_p4_note = '''
Note : Plotly affiche les 8 premiers jours de données à la fin de la période pour une raison inconnue, trier
les données a conduit à une disparition de la barre sur l'Afrique, nous avons donc laissé les données telles quelles.
'''

txt_p5 = '''
On constate que l'Amérique du Nord est la première zone géographique à avoir reçu une vaccination. L'Europe arrive
rapidement derrière puis l'Asie qui rattrapent rapidement leur retard. L'Océanie arrive plus tard et rattrape
également sont retard. Quatre continents obtiennent une population vaccinée à plus de 60% au bout de 1 an.
Cependant l'Afrique reste en marge de la vaccination, avec un taux de seulement 14.13% au bout d'un an également. 
'''

txt_p6 = '''
On affiche ci-dessous un graphique qui représente le pourcentage de population vaccinée en fonction du PIB par
habitant (en échelle logarithmique) à la date du 1er janvier 2022, soit 1 an après le début de la campagne de
vaccination dans la plupart des pays occidentaux. Ce dernier ce calcul avec un produit en croix entre le nombre
de personnes vaccinées et le pourcentage de personnes vaccinées (qui donne la population du pays). On affiche
également une courbe de régression de type OLS (moindres carrés) avec comme indication, que l'axe
des abscisses est en échelle logarithmique.
'''

txt_p7 = '''
On constate donc une certaine corrélation entre le PIB par habitant et le taux de vaccination de la population.
Ceci dit, le coefficient de corrélation est de 0.59, ce qui est assez faible. Cette tendance est impactée par les
programmes d'aides humanitaires tels que Covax, qui ont pour but d'assurer un accès équitable à la vaccination
contre le Covid-19 dans 200 pays, avec les pays les plus précaires en priorité.
'''
