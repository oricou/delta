# Rendu pour le projet de PYBD - Jules Dorbeau et Noé Jenn-Treyer, SCIA 2023

Voici notre rendu pour ce projet de création d'une application Dash afin de réaliser une présentation sur des données. 

Nous avons choisit de faire cela sur l'étude de l'évolution des polluants en France, l'environnement étant une des problématiques les plus importantes du moment, si ce n'est la plus importante.

## Visualisation de notre projet : 

Pour pouvoir voir ce que donne notre projet, deux options sont possibles : utiliser l'application que nous avons déployée via le lien que avons fourni, ou lancer le code sur votre ordinateur pour pouvoir le visualiser en local.

### Première option : 

La première est de passer par ce lien qui vous donnera accès directement à notre application dash que nous avons déployée : 

https://dash-pybd-jules-dorbeau.herokuapp.com/

(Le chargement peut prendre un peu de temps)

### Deuxième option : 

La deuxième est directement lancer nos deux fichiers .py avec Python.

Pour cela voici les étapes à suivre : 

Pour commencer, il vous faudra installer les librairies requises pour ce projet avec le ficher requirements situé à la racine du git :
    
    pip install -r requirements.txt

La suite se déroulera dans le dossier de notre projet :

    cd JD_NJ_Etude_de_la_pollution

Ensuite, ayant déjà fourni les données traitées, vous n'avez pas forcément besoin de passer par la partie de traitement des données qui est la suivante (qui peut prendre autour de 15 minutes) :

    python3 get_data.py
    
Ce fichier va décompresser toutes les données brutes qui sont présentes sous la forme de 12 dossiers compressés (1 par mois) afin de complètement les traiter. Ayant une grande quantité de donnée, ce qui rend le traitement assez long, nous avons laissé les données utilisées par l'application afin d'éviter de devoir le faire. Lors du traitement, de plus, nous gérons la suppression des fichiers des données brutes et temporaires afin de ne pas conserver des données inutilement. Vous n'aurez donc à la fin que les fichiers utilisés dans le dossier data.

Ensuite pour finir pour lancer l'application en local, vous n'avez qu'à lancer la commande suivante : 

    python3 dash_app_pollution.py
    
Ensuite, vous n'aurez qu'a vous connectez sur le site suivant : http://127.0.0.1:8051/

Vous pourrez donc ainsi librement vous servir de notre projet de la façon dont vous le souhaitez !

## Liens : 

Lien de notre projet déployé : https://dash-pybd-jules-dorbeau.herokuapp.com/

Lien de nos données brutes : https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/2021/

Lien du projet Delta : https://delta.lrde.epita.fr/