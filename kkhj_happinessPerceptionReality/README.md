# Δelta δata

### Perception VS. Reality

Le projet Bonheur Réel versus Bonheur Perçu a pour but de comparer le bonheur receuilli dans un sondage, qui correspond donc au bonheur perçu, à celui calculé à partir de certains indicateur économiques et sociaux, permettant de quantifier la pyramide des besoins, tout en laissant la liberté à l'utilisateur d'indiquer l'importance de chaque paramètre. 

### Récupération de données

La fonction `get_data()` de `get_data.py` permet de récupérer le tableau final sur lequel est basé nos graphiques. Elle rassemble toutes les bases de données retrouvées en ligne (pour plus de détail, merci de cliquer sur les liens dans Sources à la fin d'interface)

Les fichiers python dont le nom commence par `clean` permettent d'extraire ces données et de les nettoyer. Pour accéder directement aux datasets sources, il suffit d'appeler la première fonction de chaque fichier `clean*data.py`.

### Source Code

Le jeux de données est composé de plusieurs fichiers excel et csv, receuilli sur différents sites (cf. sources).

Pour exécuter le code, il suffit d'exécuter le ficher `delta.py` et de cliquer sur `Conception du Bonheur` dans la liste des projets.
Il sera alors possible de modifier le pourcentage des quatres paramètres pris en considération (en haut à gauche de l'interface) et de voir évoluer l'indice du bonheur.


##### P.-S.: la base de donnée pour illustrer le critère « niveau d’éducation » ne contient pas assez de données. Nous avons donc décider de ne pas l'inclure afin d'avoir un nombre considérable de pays représentés. Nous avons mis les parties concernées dans les commentaires `TODO`.  Lorsqu’une nouvelle base de donnée plus complète est trouvée, il suffira simplement de décommenter les lignes concernées pour intégrer ce critère.
