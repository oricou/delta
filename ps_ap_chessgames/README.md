# Chess δata  
* Pour entrer dans l'environement virtuel:  
  * Entrez en ligne de commandes:  
     * `poetry install`
       * Si le poetry install fail à cause de Scipy (une des dépendences du prof) c'est probablement parce que vous n'avez pas de compilateur fortran, pour en installer un vous pouvez faire "`sudo apt-get install gfortran`" ou "`yay -S gcc-fortran`" si vous êtes sur linux 
  * Entrez ensuite:  
    * `poetry shell` 

* Pour télécharger et extraire les données entrez:  
  * `python get_data.py`    
  
* Pour visualiser les données:
  * Lancez le serveur web en vous plaçant dans delta/ et en entrant:
    * `make run`
  * Allez ensuite à l'url suivante: [127.0.0.1:8050/](127.0.0.1:8050/)
