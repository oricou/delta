# Δelta δata

### Analyse de données ouvertes

L'exercice consiste à prendre des données ouvertes et à les mettre en forme pour aider à l'analyse. Cela peut se faire
sous forme d'articles avec des graphiques (voir les feuilles Jupyter dans le dépôt) ou de graphiques interactifs (
voir  https://delta.lrde.epita.fr/).

### Code source

Ce dépôt GitHub propose des pages Jupyter et des service Dash pour analyser des données ouvertes. Les sous-dépôts sont :

* [Natalité / revenus](https://github.com/oricou/delta/tree/main/population) : exemple classique qui montre la chute de
  natalité à travers le monde et la croissance des revenus
* [Prix de l'énergie](https://github.com/oricou/delta/tree/main/energies) : compare le prix grand public de différentes
  énergies en France
* [Sondages présidentiels et temps de parole dans les médias](https://github.com/nsppolls/nsppolls/blob/master/presidentielle.csv) :
  compare le temps de parole des candidats dans les médias et dans les intentions de vote données grâce aux différents
  sondages.

### Get Data

Le fichier `get_data.py` permet de récupérer les données depuis un lien et de les transformer pour notre utilisation.
Exécuter ce fichier mettra à jour les données.

Note : le choix du français est volontaire, il s'agit de promouvoir l'usage
des données ouvertes auprès du grand public en France. Cela étant il
est possible d'en faire une version dans une autre langue.
