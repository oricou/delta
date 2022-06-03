import pandas as pd

#https://www.insee.fr/fr/statistiques/4487837
#https://www.insee.fr/fr/statistiques/fichier/4487837/2022-01-28_deces_quotidiens_departement.zip
url_mort = "2022-01-28_deces_quotidiens_departement.xlsx"
Excel_mort = pd.ExcelFile(url_mort)
mort_france = pd.DataFrame({"Numéro département": [], "Morts": []})

for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
           '2A', '2B', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
           '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
           '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
           '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', 'France']:
    mort_france.loc[i] = [i, pd.read_excel(Excel_mort, i).iat[368, 6]]

mort_france = mort_france.set_index('Numéro département').rename(index = {'France' : 'Total'})


#https://www.insee.fr/fr/statistiques/2012717
url_salaire = "https://www.insee.fr/fr/statistiques/fichier/2012717/TCRD_022.xlsx"
#url_salaire = "TCRD_022.xlsx"
Excel_salaire = pd.ExcelFile(url_salaire)

salaire = pd.read_excel(Excel_salaire, 'DEP').rename(columns = {
    "Ménages fiscaux et revenu disponible en 2019 : comparaisons départementales": "Numéro département",
    'Unnamed: 1' : 'Département',
    'Unnamed: 2' : 'Nombre de ménages fiscaux',
    'Unnamed: 3' : 'Ménages fiscaux imposés (en %)',
    'Unnamed: 4' : 'Revenu médian'
}).set_index('Numéro département').drop(index = [
    '972',
    '974'
], columns = [
    'Unnamed: 5',
    'Unnamed: 6'
]).dropna().rename(index = {
    'M': 'Total'
})


tot = pd.merge(mort_france, salaire, how = 'left', on='Numéro département')
tot = tot[['Département', 'Morts', 'Nombre de ménages fiscaux', 'Ménages fiscaux imposés (en %)', 'Revenu médian']]
list = []
for i in range (0, 97):
    list.append(tot.iat[i, 4] / tot.iat[i, 1])
tot['revenu/morts'] = list
