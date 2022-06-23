# Projet d'analyse de foot

Le but de notre projet était de montrer la corrélation entre la valeur marchande des équipes, l'âge moyen de ses joueurs et ses résultats dans leur ligue (Top 5 ligues).

### Préparation de la donnée:

Dans le dossier data, il y a le dossier AgesJoueurs qui correspond à l'âge de tous les joueurs de chaque club des top 5 ligues (de 2004 à 2021). 
Dans ce dossier vous avez également les dossiers liga, PL, bundeshliga, ligue1 et serieA. Dans ces derniers, vous avez les classements de chaque ligue de 2004 à 2021. 

Les dossiers AverageAges, concat, concat_leagues, concat_years et concat_years_age et concat_leagues. Ces dossiers contiennent des fichiers csv crées par nous même en codant. 

Dans le dossier concat, chaque fichier correspond à la concaténation de toutes les saisons (de 2004 à 2021) de chaque ligue.

Le dossier concat_years est presque comme le dossier concat. Nous avons seulement ajouter une colonne years qui correspond à la saison. Dans le dossier concat_years_age nous avons ajouté une colonne Age qui correspond à l'âge moyen des joueurs de chaque club. 

Dans le dossier concat_leagues nous avons un fichier qui correspond à la concaténation de tous les fichiers de concat_years_age, c'est à dire le classement des 5 ligues de 2004-05 à 2020-21, avec les colonnes Age et years. 

### Qu'est ce que la valeur marchande d'une équipe ? 

La valeur marchande d'un joueur est une estimation du montant pour lequel une équipe peut vendre le contrat du joueur à une autre équipe. Grace à https://www.transfermarkt.com/ nous avons réussi à récupérer la valeur marchande de chaque club. 
