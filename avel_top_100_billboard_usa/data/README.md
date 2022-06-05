# Informations sur le téléchargement des données

Les données sont disponibles sur le
site [Kaggle - Billboard "The Hot 100" Songs](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs)

Elles ne sont pas téléchargées par le script puisqu'il est nécessaire de passer par l'API de Kaggle.

Bien que les données soient en libre accès, il est nécessaire de posséder un token d'identification
et donc, d'un compte gratuit pour pouvoir télécharger les données.

Le module Python `kaggle` est disponible [sur pypi (pip)](https://pypi.org/project/kaggle/) mais n'est pas utilisable
dans le
projet puisqu'il n'est pas autorisé de rajouter des dépendances.

Si cela était possible, l'import se ferait de la manière suivante (en bash ou dans un script iPython avec un `!` devant
chaque commande):

```bash
kaggle datasets download -d dhruvildave/billboard-the-hot-100-songs --unzip
mv charts.csv top_100_billboard_usa.csv
```

Il est également possible de télécharger les données en important le module dans python.
Cela n'est cependant pas officiellement supporté par Kaggle et est plus complexe.