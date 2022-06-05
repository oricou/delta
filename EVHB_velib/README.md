# Les vélibs

Nous nous sommes intéressés à l'utilisation des vélibs dans l'Île-de-France. \
Peut-on clairement discerner des pics d'utilisation ainsi que des creux ?

Laissons parler les données.

## Aspiration des données

Nous avons accès aux données [opendata.paris](https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/?disjunctive.name&disjunctive.is_installed&disjunctive.is_renting&disjunctive.is_returning&disjunctive.nom_arrondissement_communes). \
Nous avons donc cherché à les mettre à profit. \
Problème : Ces données sont des données temps réel, et donc des données à un instant T.

Nous avons donc fait un script Python d'aspiration des données situé dans `./data/`, nommé `fetch.py`. \
Les données aspirées se retrouvent dans le dossier `./data/velib/`, les fichiers suivant cette norme de nommage : `AAAA_MM_JJ_HH_MM_velib.csv`. \
Pour un accès direct aux données, cliquer [ici](https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B). \
On a récupéré les données sur la plage 14h54 le 10 mars 2022 - 16h17 le 12 mars 2022.

Cela nous donne une journée complète à exploiter, le 11 mars 2022. Ce que nous ferons ensuite.

## Traitement des données

Les fichiers récupérés contiennent des informations sur le bornes des vélibs. Nous ne disposons seulement que de leur identifiant. \
Il nous faut un système pour les regrouper par département.

### Données annexes

#### GeoJSON

Nous avons récupéré les données des communes, grâce à [GeoJSON](https://france-geojson.gregoiredavid.fr/), plus précisément sur ce [lien](https://france-geojson.gregoiredavid.fr/repo/regions/ile-de-france/communes-ile-de-france.geojson).

#### Population

Nous avons aussi eu besoin des données de population par commune et arrondissement. \
Nous avons utilisé cette [api](https://public.opendatasoft.com), plus précisément, ce [point terminal](https://public.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut)

### Nettoyage

La première chose à faire était de retirer les colonnes ainsi que les renommer.
Le script dans `./data/`, nommé `clean_csv.py` s'en est chargé.
Ce script récupère aussi les informations sur les polygones de chaque commune et assigne une borne à celles-ci.

### Groupement

On souhaite désormais récupérer les données concernant chacune des communes, et non pas des bornes individuelles. \
On a regroupé les données grâce au script dans `./data/`, nommé `groupby.py`. Les données sont donc groupées par arrondissement et commune.

### Lier nos données vélibs aux données de population

Le script dans `./data/`, nommé `connect_data.py` s'en est chargé. \
Il récupère les données groupées et assigne à chaque arrondissement et commune sa population. \
Il rajoute dans notre dataframe final plusieurs clés afin de tester quelle méthode met en avant nos résultats

Le ratio de vélibs disponibles :

- `ratio_pop` par rapport à la population.
- `ratio_pop_log2` par rapport à la population, log2.
- `ratio_pop_log10` par rapport à la population, log10.
- `ratio_avail` par rapport au nombre d'emplacements vélibs au sein de la commune / arrondissement.
- `ratio_avail_log2` par rapport au nombre d'emplacements vélibs au sein de la commune / arrondissement, log2.
- `ratio_avail_log10` par rapport au nombre d'emplacements vélibs au sein de la commune / arrondissement, log10.
- `ratio_avail_glob` par rapport au nombre d'emplacements de vélibs total.

Au final nous avons choisi la clé `ratio_avail` pour montrer nos données.

### Fluctuations

Pour montrer au mieux les fluctuations dans les usages de vélib, nous avons calculé, à l'aide du script dans `./data/`, nommé `difference.py`, le delta de vélibs disponibles entre deux instants (toutes les 30 minutes).

## Conclusion

![Usage des vélibs](./usage.png)

On remarque grâce à ce graphique, qu'il y a bien des heures de pointes, deux le matin et une le soir.
