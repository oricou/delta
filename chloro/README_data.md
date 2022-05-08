# Récupération des données brutes

Les données brutes sont récupéréer à l'aide de deux services de COPERNICUS :
COPERNICUS Marine Service pour la chlorophylle et COPERNICUS Land Service pour
le FAPAR.

Malheureusement pour accèder aux données disponibles sur les sites dédiés à ces
services il est nécessaire de créer un compte gratuit pour chacun d'entre eux.
Cela empêche de pouvoir récupérer les données dans un script python, il faut
les récupérer à la main.

Ce document décrit les étapes nécessaires à la récupération des données brutes (~2 Go au total).

### COPERNICUS Marine Service

Afin de récupérer les données sur la chlorophylle :

* Créer un compte sur COPERNICUS Marine Service (gratuit, 5 mn) : https://resources.marine.copernicus.eu/registration-form

* BIEN PENSER à activer le compte par mail avant de poursuivre le processus

* Exécuter les commandes suivantes en remplacant \<login\> et \<password\> par le login et password du compte que vous venez de créer :

```bash
motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id GLOBAL_MULTIYEAR_BGC_001_029-TDS --product-id cmems_mod_glo_bgc_my_0.25_P1D-m --longitude-min -180 --longitude-max 179.75 --latitude-min -80 --latitude-max 90 --date-min "2019-06-11 12:00:00" --date-max "2019-06-20 12:00:00" --depth-min 0 --depth-max 15 --variable chl --out-dir "." --out-name "CHL_summer.nc" --user "<login>" --pwd "<password>"
```

```bash
motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id GLOBAL_MULTIYEAR_BGC_001_029-TDS --product-id cmems_mod_glo_bgc_my_0.25_P1D-m --longitude-min -180 --longitude-max 179.75 --latitude-min -80 --latitude-max 90 --date-min "2019-12-11 12:00:00" --date-max "2019-12-20 12:00:00" --depth-min 0 --depth-max 15 --variable chl --out-dir "." --out-name "CHL_winter.nc" --user "<login>" --pwd "<password>"
```

* Déplacer les données téléchargées (fichiers en .nc) dans le dossier chloro/data

### COPERNICUS Land Service

Afin de récupérer les données sur le FAPAR :

* Créer un compte sur COPERNICUS Land Service (gratuit, 5 mn) : https://land.copernicus.vgt.vito.be/PDF/portal/Application.html#Home

* BIEN PENSER à activer le compte par mail avant de poursuivre le processus 

* Accéder au lien de téléchargement suivant, entrer ses identifiants, et télécharger le fichier de données en .nc (en dessous de Data files) : https://land.copernicus.vgt.vito.be/PDF/free?productID=50080173&collectionID=1000084 

* Renommer le fichier téléchargé en "FAPAR\_summer.nc" puis le déplacer dans chloro/data

* Répéter la procédure de téléchargement pour les données hivernales à l'aide de ce lien : https://land.copernicus.vgt.vito.be/PDF/free?productID=56836343&collectionID=1000084

* Renommer le fichier téléchargé en "FAPAR\_winter.nc" puis le déplacer dans chloro/data





