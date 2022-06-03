Etude de la qualité de vie des gens en fonction de leur temps de travail moyen par pays
par Tanguy Desgouttes et Marc-Emmanuel Raiffe


Vous pourez trouver dans ce projet 4 graphiques qui montrent :
    - la note moyenne de satisfaction dans la vie en fonction du temps de travail hebdomadaire moyen par pays
    - la proportion de symptomes dépressifs en fonction du temps de travail hebdomadaire moyen par pays
    - l'espérance de vie en fonction du temps de travail hebdomadaire moyen par pays
    - la fréquence de sentiment de bonheur en fonction du temps de travail hebdomadaire moyen par pays

Ci-joint la structure complète du projet (fichiers trop lourds non inclus dans le répertoire final compris) :

tdmr_quality_of_life_and_worktime/
   - data/
       - life_satistaction_eu_clean.csv
       - life_expectancy_eu_clean.csv
       - hapiness_feelings_frequency_eu_monthly_clean.csv
       - depressive_symptoms_eu_clean.csv
       - average_worktime_eu_weekly_clean.csv
       - life_satistaction_eu.csv
       - life_expectancy_eu.csv
       - hapiness_feelings_frequency_eu_monthly.csv
       - depressive_symptoms_eu.csv
       - average_worktime_eu_weekly.csv
       - get_data.py
   - tdmr_quality_of_life_and_worktime.py
   - README.md


toutes les sources viennent de https://ec.europa.eu/eurostat/fr/web/main/data/database :

https://ec.europa.eu/eurostat/databrowser/view/LFSA_EWHUN2__custom_2616289/default/table?lang=fr
https://ec.europa.eu/eurostat/databrowser/view/ILC_PW01__custom_2616313/default/table?lang=fr
https://ec.europa.eu/eurostat/databrowser/view/HLTH_EHIS_MH1E__custom_2627991/default/table?lang=fr
https://ec.europa.eu/eurostat/databrowser/view/demo_mlexpec$DV_292/default/table?lang=fr
https://ec.europa.eu/eurostat/databrowser/view/ilc_pw08$DV_426/default/table?lang=fr

les données complètes sont exportables mais trop lourdes pour être postées sur github, le fichier get_data fait état des transfomation apportées pour produire les bases de données propres.