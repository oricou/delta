Projet effectué par Martin Poulard et Grégoire Grégroire Gally. 

Nous avons exploité la base de donnés du National Climatic Data Center (USA), elle rassemble des donnés météorologiques de miliers de station. Ces donnés sont classés par station sous forme de csv. Notre but va etre d'analyser.

Les donnés journalières sont stockés initalement dans "daily reports", leru inventaire est fait par le fichier "stations". On va créer un dataframe afin de rassembler les mesures qui nous interessent. Pour cela il faut lires les fichier (c'est très long, c'est pour cela que nous avons mis en place un process pool), et ne garder que les informations utiles (le type de mesure: précipitations et laps de temps des mesures en annés).

Une fois cela effectué ce dataframe est découpé par annés et sauvegardé dans un dossier afin de ne pas avoir à refaire l'opération à chaques fois.

Le dossier géodata contient un fichier géojson. Celui ci rassemble les point nessécaires pour de faire le contour des différents états (sous forme de polygone) afin de pouvoir faire une carte avec une valeur par état. 

Le fichier "allocations trades" contient les échanges d'eau ainsi que leurs prix. 

Pour une raison de performance, toutes ces opérations sont faites au préalable et les dataframes sont enregistrés au format pickle dans les répertoire. 