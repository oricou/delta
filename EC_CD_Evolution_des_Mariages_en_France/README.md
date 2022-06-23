# Evolution of Mariages in France

This visualization allows to see the evolution of the numbers of mariages in France since 1946.

## Elements :
* A map of France that activates starting 2014
* A histogram showing the number of mariages by month before 2014
* The same histogram showing the number and type of mariages (homosexual or heterosexual) by month and department starting 2014
* A graph showing the general evolution of the number of mariages since 1946 to 2020
* A slider to scroll the years
* A button to activate/deactivate the automatic scroll of the years (and department starting in 2014)
* Sources

## Run the visualisation

1) Install python 3.10.4
2) Install required packadge with :
    ```
    pip install -r requirements.txt
    ```

3) Launch the dash server at the root of the project:
    ```
    make run
    ```

## Data
To create the file used by the project, go inside data and launch the script get_data.py:
    ```
    python3 get_data.py
    ```

### Authors
* Elodine Coquelet
* Calliopee Desenfans
