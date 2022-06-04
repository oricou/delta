## Sujet: Les inégalités de revenus dans le monde

Nous avons cherché à déterminer si les inégalités de revenus dans un pays pouvaient être corrélées avec:
- Le niveau de corruption du pays (Période d'étude: 1995 et 2020)
- Le niveau de démocratie du pays (Période d'étude: 2006 et 2020)
- Le produit intérieur brut par habitant (Période d'étude: 1995 et 2020)

Nous avons un graphique principal permettant de sélectionner les données que l'on souhaite croiser.
Sur l'axe des ordonnées pour comparer les inégalités de revenus entre les pays, on peut sélectionner la part des revenus détenue par une certaine portion de la population d'un pays (1% des plus riches, 10% des plus riches, 50% des plus pauvres, 10% des plus pauvres) ou le coefficient de Gini. Il est également possible de sélectionner un pays pour obtenir l'évolution des axes sur l'ensemble de la période étudiée.

Structure:
```sh
mzgl_inegalites_de_revenus/
   - data/
     - Corruption_perceptions_index/
     - GDP/
     - Population/
     - wid_data/
     - Democracy_indices.csv
   - get_data.py
   - mzgl_inegalites_de_revenus.py
   - README.md
```
### Concernant les fichiers de données
Ils ont été téléchargés en amount et placés dans l'archive "data.zip", car il n'était pas possible de télécharger
l'ensemble des données. Il y avait, de plus, beaucoup trop de fichiers inutiles.
Les CSV n'ont pas été modifiés à la main.

Sources:
- [Population, Banque mondiale](https://data.worldbank.org/indicator/SP.POP.TOTL?name_desc=false)
- [PIB par personnes, Banque mondiale](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)
- [Inégalités de revenus, World inegalities database](https://wid.world/data/)
- [Index de corruption, Transparency International](https://www.transparency.org/en/cpi/2021)
- [Index de démocratie, Gapminder](https://www.gapminder.org/data/documentation/democracy-index/)

Auteurs: Gauthier Lombard & Mathieu Zimmermann