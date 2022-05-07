# Ce fichier contient le texte des éléments HTML afin de ne pas encombrer le fichier principal

txt_title = 'Vaccinations contre le COVID-19 par pays en fonction du temps'

txt_p1 = '''
On va présenter ci-dessous les liens entre les taux de vaccinations contre le COVID-19 et le PIB des pays.
Pour simplifier les résultats, nous ne garderons les données qu'à partir du 1er janvier 2021 (inclus). Les données
du PIB datent de 2016 car aucune donnée n'était disponible pour tous les pays au dela de cette année-là.
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
affichées.<br>
<i>Note :</i> Plotly affiche les 8 premiers jours de données à la fin de la période pour une raison inconnue, trier
les données a conduit à une disparition de la barre sur l'Afrique.
'''

txt_p5 = '''
On constate que l'Amérique du Nord est la première zone géographique à avoir reçu une vaccination. L'Europe arrive
rapidement derrière puis l'Asie qui rattrapent rapidement leur retard. L'Océanie arrive plus tard et rattrape
également sont retard. Quatre continents obtiennent une population vaccinée à plus de 60% au bout de 1 an.
Cependant l'Afrique reste en marge de la vaccination, avec un taux de seulement 14.13% au bout d'un an également. 
'''
