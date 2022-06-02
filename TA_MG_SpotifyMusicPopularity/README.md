## SUJET : Mise en valeur des caractéristiques musicales qui influent sur la popularité d'une musique

L'objectif de cette étude était d'identifier des caractéristiques qui peuvent déterminer si une musique est populaire sur un jeu de données de Spotify.
Les caractéristiques déterminées par Spotify pour catégoriser une musique sont les suivantes :
        - L'acousticité : détermine la qualité sonore en fonction des vibrations par example le bruit.
        - La dansabilité : basée sur la combinaison des éléments musicaux suivants (tempo, stabilité du rythme, puissance du tempo, régularité sonore).
        - La durée en ms
        - L'énergie : perception de l'intensité et du dynamisme de la musique, une musique trés énergique va parraître bruyant et rapide.
        - L'instrumentalité : détermine si une musique ne contient pas de paroles, les onomatopées ne sont pas considérées comme des paroles.
        - La vivacité : détermine s'il y a une audience dans la musique. Une musique en live aura une vivacité très élevèe.
        - L'intensité sonore
        - La quantité de paroles : doit être inférieure à 66% pour être considérée comme une musique.
        - Le tempo
        - La valence : détermine si une musique est positive (++ euphorie, joie || -- tristesse, colère).

Notre première database fournit les informations sur les caractéristique des musiques tandis que la seconde fournit le pays d'origine, le nombre d'écoute, la trend des musiques.

Un diagramme à bulles est le diagramme principale sur lequel on peut comparer les caractéristiques des genres entre elles en choisissant une caractéristique et en la confrontant avec la popularité.
On a la possibilité d'adapter le diagramme en fonction de la moyenne sur un échantillon des 10 ou 10 000 meilleures musiques de chaque genres.
Un sous-diagramme polaire permet de résumer le genre séléctionné dans le diagramme à bulles.

### Ce que l'on peut en déduire :
- On observe grâce à ces diagrammes que certainnes caractéristiques sont importantes pour qu'une musique soit populaire : la dansabilité, l'énergie et la valence. On peut prendre l'exemple du Rap ou de la Pop.
- On observe aussi que certains genre sont des genres de "niche" qui se base souvent sur une carctéristique. On peut prendre l'exemple de l'Opéra ou des musiques de films.
- Les restes des caractéristiques influent moins sur la popularité mais permettent de déterminer le type d'une musique. On peut prendre l'exemple de la quantité de parole.

### Structure :
```sh
spotify/
    - data/
        - data.tar.gz
        - get_data.py
    - Popularité des musiques.ipynb
    - spotify.py
    - README.md
```

### SOURCE :
    -   [Caractéristiques et popularité des musiques de Spotify](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) sur kaggle.com
    -   [Informations complémentaires sur la popularité, la date, ou la région](https://www.kaggle.com/datasets/dhruvildave/spotify-charts) sur kaggle.com

### AUTEUR :
    -   Melvin Gidel
    -   Thibaut Ambrosino
