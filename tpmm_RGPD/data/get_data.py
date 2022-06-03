import pandas as pd
import numpy as np

# 1. nb_notif vs nb_dpo

## Notifications

### Load BD
data  = pd.read_excel("./1. nb_notif vs nb_dpo/notifications-open-data-20211201.xls")

### Définition des indexes et nom de colonnes
data.columns = data.iloc[0]
data = data.drop(index=0)
data.columns = ['date_notification', 'secteur_d_activite', 'natures_violation', 'nombre_personnes', 'type_donnees_impactees', 'donnees_sensibles', 'origine_incident', 'causes_incident', 'personnes_informees']

### Clean des donnés
data.drop(['natures_violation', 'nombre_personnes', 'type_donnees_impactees', 'donnees_sensibles', 'origine_incident', 'causes_incident', 'personnes_informees'], axis = 1, inplace = True) 
data.date_notification = pd.to_datetime(data.date_notification)
data.secteur_d_activite = data.secteur_d_activite.astype('category')

nomenclature_INSEE = [["A", "Agriculture, sylviculture et pêche"], ["B", "Industries extractives"],
                      ["C", "Industrie manufacturière"],
                      ["D", "Production et distribution d'électricité, de gaz, de vapeur et d'air conditionné"],
                      ["E", "Production et distribution d'eau ; assainissement, gestion des déchets et dépollution"],
                      ["F", "Construction"], ["G", "Commerce ; réparation d'automobiles et de motocycles"],
                      ["H", "Transports et entreposage"], ["I", "Hébergement et restauration"],
                      ["J", "Information et communication"], ["K", "Activités financières et d'assurance"],
                      ["L", "Activités immobilières"], ["M", "Activités spécialisées, scientifiques et techniques"],
                      ["N", "Activités de services administratifs et de soutien"], ["O", "Administration publique"],
                      ["P", "Enseignement"], ["Q", "Santé humaine et action sociale"],
                      ["R", "Arts, spectacles et activités récréatives"], ["S", "Autres activités de services"],
                      ["T", "Activités des ménages en tant qu'employeurs ; activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre"],
                      ["U", "Activités extra-territoriales"], ["X", "Inconnu"]]
INSEE_to_secteur = {insee: secteur for insee, secteur in nomenclature_INSEE}
secteur_to_INSEE = {secteur: insee for insee, secteur in nomenclature_INSEE}

data.secteur_d_activite = data.secteur_d_activite.cat.rename_categories({
    "Activités des ménages en tant qu''employeurs ; activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre" : "Activités des ménages en tant qu'employeurs ; activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre",
    "Activités financières et d''assurance" : "Activités financières et d'assurance",
    "Commerce ; réparation d''automobiles et de motocycles" : "Commerce ; réparation d'automobiles et de motocycles",
    "Production et distribution d''eau ; assainissement, gestion des déchets et dépollution" : "Production et distribution d'eau ; assainissement, gestion des déchets et dépollution",
    "Production et distribution d''électricité, de gaz, de vapeur et d''air conditionné" : "Production et distribution d'électricité, de gaz, de vapeur et d'air conditionné"
})

data.secteur_d_activite = data.secteur_d_activite.cat.rename_categories(secteur_to_INSEE)

### Regroup data
data_notification = data.groupby(["date_notification", "secteur_d_activite"]).size()
data_notification = data_notification.unstack()
data_notification = data_notification.reindex(sorted(data_notification.columns), axis=1).sort_index()

## Save notifications
data_notification.to_pickle("1_data_notification.pkl")


## DPOs

### Load BD
data = pd.read_excel("./1. nb_notif vs nb_dpo/opencnil-organismes-avec-dpo.xlsx")

### Définition des indexes et nom de colonnes
data.columns = data.iloc[0]
data = data.drop(index=0)
data.columns = ['siren_designant', 'nom_organisme_designant', 'secteur_d_activite_designant', 'naf_designant', 'adresse_postale_designant', 'code_postal_designant', 'ville_designant', 'pays_designant', 'type_dpo', 'date_designation', 'siren_designe', 'nom_organisme_designe', 'secteur_d_activite_designe', 'naf_designe', 'adresse_postale_designe', 'code_postal_designe', 'ville_designe', 'pays_designe', 'dpo_email', 'dpo_url', 'dpo_tel', 'dpo_adresse_postale', 'dpo_code_postal', 'dpo_ville', 'dpo_pays', 'dpo_autre']

### Clean des donnés
data.drop(['siren_designant', 'nom_organisme_designant', 'naf_designant', 'adresse_postale_designant', 'code_postal_designant', 'ville_designant', 'pays_designant', 'type_dpo', 'siren_designe', 'nom_organisme_designe', 'secteur_d_activite_designe', 'naf_designe', 'adresse_postale_designe', 'code_postal_designe', 'ville_designe', 'pays_designe', 'dpo_email', 'dpo_url', 'dpo_tel', 'dpo_adresse_postale', 'dpo_code_postal', 'dpo_ville', 'dpo_pays', 'dpo_autre'], axis = 1, inplace = True)
data.date_designation = pd.to_datetime(data.date_designation.str[3:], format='%m/%Y')
data.columns = ['secteur_d_activite', 'date_designation']
data.secteur_d_activite = data.secteur_d_activite.fillna('X')
data.secteur_d_activite = data.secteur_d_activite.astype('category')

### Regroup data
data_dpo = data.groupby(["date_designation", "secteur_d_activite"]).size()
data_dpo = data_dpo.unstack()
data_dpo = data_dpo.reindex(sorted(data_dpo.columns), axis=1).sort_index()

## Unifier les dates
data_dpo = data_dpo.loc[:'2021-08']

## Save dpos
data_dpo.to_pickle("1_data_dpo.pkl")



# 2. budget_cnil vs sanctions

## Budget de la CNIL

### Load BD
budget_cnil = pd.read_excel("./2. budget_cnil vs sanctions/opencnil-budget-depuis-2000-maj-2021.xlsx", index_col=0)

### Clean des donnés
budget_cnil = budget_cnil.transpose()
budget_cnil.drop(budget_cnil.columns.difference(["Budget total"]), axis=1, inplace=True)

### Définition des nom de colonnes
budget_cnil.columns = ["budget_cnil"]


## Sanctions

### Load BD
dfs = pd.read_html("https://www.cnil.fr/fr/les-sanctions-prononcees-par-la-cnil")

### Définition nom de colonnes et clean des collonnes
for df in dfs:
    if df.columns[0] == "Date":
        df.columns = ['date', 'nom_type_orga', 'manquements', 'decision']
        df.drop(['nom_type_orga', 'manquements'], axis = 1, inplace = True)
    else:
        df.columns = ['date', 'nom_type_orga', 'theme', 'manquements', 'decision']
        df.drop(['nom_type_orga', 'theme', 'manquements'], axis = 1, inplace = True)

### Merge datas
sanctions_df = {}
for df in dfs:
    year = int(df["date"][0].split('/')[-1])
    sanctions_df[year] = df

sanctions = pd.concat(sanctions_df)

### Définition des types
sanctions['date'] = pd.to_datetime(sanctions['date'], errors='coerce', format='%d/%m/%Y')
sanctions.drop(sanctions[sanctions['date'].isna()].index, inplace = True)

### Définition des indexes
sanctions.set_index("date", append=True, inplace=True)
sanctions.reset_index(level=1, drop=True, inplace=True)

### Get sanctions amount
sanctions['decision'] = sanctions['decision'].str.encode('ascii', 'ignore').str.decode('ascii')
sanctions = sanctions[sanctions['decision'].str.contains("pcuniaire", case=False)]
sanctions['decision'] = sanctions['decision'].str.replace('.',' ', regex=False)
sanctions['amount'] = np.nan

selection = sanctions['decision'].str.contains("\(.* euros?\)", regex=True)
sanctions['amount'][selection] = sanctions['decision'][selection].str.extract("\((.*) euros?\)")[0].str.replace(" ", "").astype('int')

selection = sanctions['amount'].isna() & sanctions['decision'].str.contains("de [0-9 ]+ euro", regex=True)
sanctions['amount'][selection] = sanctions['decision'][selection].str.extract("de ([0-9 ]+) euro")[0].str.replace(" ", "").astype('int')

selection = sanctions['amount'].isna() & sanctions['decision'].str.contains("pcuniaire non publique", regex=True)
sanctions['amount'][selection] = 0

amounts = {
    2020: {'2020-12-07': [100000000, 35000000]},
    2019: {'2019-10-10' : [0],
           '2019-12-30': [0]},
    2018: {'2018-01-08': [100000],
           '2018-05-07': [250000],
           '2018-06-21': [75000],
           '2018-07-24': [50000, 30000, 0],
           '2018-09-06': [30000, 10000],
           '2018-12-19': [400000],
           '2018-12-26': [250000]},
    2017: {'2017-04-13': [15000],
           '2017-04-27': [150000],
           '2017-05-18': [10000],
           '2017-06-15': [1000],
           '2017-07-18': [40000],
           '2017-11-16': [25000]},
    2016: {'2016-12-15': [20000, 10000],
           '2016-10-13': [0],
           '2016-07-07': [30000],
           '2016-03-10': [100000]},
    2013: {'2013-01-10': [0]}
}
for year, days_amounts in amounts.items():
    for day, amount in days_amounts.items():
        selection = sanctions['amount'].isna() & (sanctions.index == (year, pd.to_datetime(day)))
        sanctions['amount'][selection] = amount

### Drop decision collumn
sanctions.drop(["decision"], axis = 1, inplace = True)

### Group by year
sanctions = sanctions.groupby(level=0).sum()


## Merge datas
budget_cnil = budget_cnil.loc[2012:2021]
budget_cnil_sanctions = pd.merge(sanctions, budget_cnil, left_index=True, right_index=True)

### Save budget_cnil_sanctions datas
budget_cnil_sanctions.to_pickle("2_budget_cnil_sanctions.pkl")


# 3. avertissements_sanctions_mise_en_demeure vs nb_controles

## Controles

### Load BD
controles = pd.read_excel("./3. avertissements_sanctions_mise_en_demeure vs nb_controles/controles-depuis-1990-maj-juin-2021.xlsx", index_col=0)

### Clean des donnés
controles = controles.transpose()
controles.drop(controles.columns.difference(["Contrôles réalisés"]), axis=1, inplace=True)
controles["Contrôles réalisés"] = controles["Contrôles réalisés"].astype(int)

### Définition des nom de colonnes
controles.columns = ["controles"]


## Avertissements et sanctions 2014 - 2018

### Load BD
sanc_avert1 = pd.read_excel("./3. avertissements_sanctions_mise_en_demeure vs nb_controles/sanctions-depuis-2014-vd.xlsx", index_col=0)

### Clean des donnés
sanc_avert1 = sanc_avert1.transpose()
sanc_avert1["sanctions"] = sanc_avert1[["Sanctions pécuniaires non publiques", "Sanctions pécuniaires publiques"]].sum(axis=1)
sanc_avert1["avertissements"] = sanc_avert1[["Avertissements non publics", "Avertissements publics"]].sum(axis=1)
sanc_avert1.drop(sanc_avert1.columns.difference(["sanctions", "avertissements"]), axis=1, inplace=True)


## Avertissements et sanctions 2019 - 2020

### Load BD
sanc_avert2 = pd.read_excel("./3. avertissements_sanctions_mise_en_demeure vs nb_controles/sanctions-depuis-2019.xlsx", index_col=0)

### Clean des donnés
sanc_avert2 = sanc_avert2.transpose()
sanc_avert2["sanctions"] = sanc_avert2.iloc[:, [0, 3, 6, 7]].sum(axis=1)
sanc_avert2["avertissements"] = sanc_avert2.iloc[:, [8, 9]].sum(axis=1)
sanc_avert2.drop(sanc_avert2.columns.difference(["sanctions", "avertissements"]), axis=1, inplace=True)


## Merge avertissements et sanctions
sanc_avert = pd.concat([sanc_avert1, sanc_avert2])

## Mise en demeure

### Load BD
mise_en_demeure = pd.read_excel("./3. avertissements_sanctions_mise_en_demeure vs nb_controles/mise-en-demeure-cnil-depuis-2014-maj-juin-2021.xlsx", index_col=0)

### Clean des donnés
mise_en_demeure = mise_en_demeure.transpose()
mise_en_demeure.drop(mise_en_demeure.columns.difference(["Total"]), axis=1, inplace=True)

### Définition des nom de colonnes
mise_en_demeure.columns = ["mise_en_demeure"]

## Merge des données
df = pd.merge(sanc_avert, mise_en_demeure, left_index=True, right_index=True)
df = pd.merge(df, controles, left_index=True, right_index=True)

## Save sanc_avert_mise_en_demeure_controles datas
df.to_pickle("3_sanc_avert_mise_en_demeure_controles.pkl")
