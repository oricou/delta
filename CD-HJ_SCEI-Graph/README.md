# SCEI Graph : 

## What is SCEI Graph?

SCEI Graph is a tool that allows you to visualize the data from the SCEI platform presenting the results of the Grandes Ecoles entrance exams. The objective of this tool is to highlight the impact of the place of training on the integration to the Grandes Ecoles.

## How to use SCEI Graph?

1. The data is already loaded, filtered and cleaned in the *data* folder. It is however possible to update them and to see how they have been processed by reading and executing the notebooks in the *notebooks* folder.
    - *extract_data.ipynb* : This notebook should be executed first. This notebook allows you to retrieve data from the SCEI platform and to group them in a usable format.
    - *enrich_data.ipynb* : This notebook allows to enrich the data with geographical coordinates.
2. This project has been tested with **python3.9.5** and the libraries that you can install with the following command
```shell
pip install -r requirements.txt
```
3. To run the project, simply run the **app.py** script.
```shell
python app.py
```

## Data sources
* https://www.scei-concours.fr/statistiques.php
* https://github.com/mhaz/SCEI-statistics/tree/master

## Authors

- **Jamet Henri** <henri.jamet@epita.fr>
- **Duchene Corentin** <corentin.duchene@epita.fr>

> Etude de l'impact du positionnement géographique des classes préparatoires et des grandes écoles sur les choix et résultats des concours d'entrée de ces dernières (SCEI)