# Energie generation in the European Union from 2000 to 2020

![](https://i.imgur.com/W7U0DlC.png)

This visualization allows to see the distribution and the evolution of the energy generation for each energy source of each country of the European Union for each year between 2000 and 2020.

## Elements of the visualization
It features:
* A map of the European Union
* A line plot
* A sunburst showing the distribution of the energy generated according to the energy source for a selected country
* Another sunburst showing the same thing but for the EU
* A drop-down menu allowing to choose the information to display on the map and on the line plot
* A radio items allowing to choose the scale (linear or logarithmic) of display on the map and the line plot
* A slider to scroll the years
* A button to activate/deactivate the automatic scrolling of the years
* A menu to select the countries to display on the map
* Sources

## Run the visualisation

### Method 1

The project has been deployed to heroku, you can find the visualisation here:
[https://eu-energy-generation.herokuapp.com/](https://eu-energy-generation.herokuapp.com/)

### Method 2

1) Install python 3.10.4
2) Install required packages

To do so, install pip and then run the following command:
```
pip install -r requirements.txt
```

3) Launch the dash server locally


Run the following command to launch the server
```
python3 Energy_generation.py
```

4) Connect to http://127.0.0.1:8050/

### Data
Data : [DataWorld, from data of Ember-Climate](https://data.world/makeovermonday/2021w5)

### Authors
* Yacine Anane
* Charli De Luca
