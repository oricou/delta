import pandas as pd

url_obesity = "https://drive.google.com/u/0/uc?id=1ABZUpC8hrf_S9D19MWUWG71BCN6H7bdI&export=download"
url_calories = "https://drive.google.com/u/0/uc?id=1cjjgbQniFlqmDzsSY-ZuyoHAQ6q3Ho68&export=download"
df_obesity = pd.read_csv(url_obesity)
df_calories = pd.read_csv(url_calories)

# Rename entity column to country
df_obesity.rename(columns = {'Entity':'Country'}, inplace = True)
# Remove useless columns in calories
df_calories = df_calories.drop(columns=['Product', 'Population', 'Production (t)', 'production__tonnes__per_capita',
                                        'Production per capita (kg)', 'Yield (t/ha)', 'Yield (kg/animal)', 'Land Use (ha)',
                                        'area_harvested__ha__per_capita','Land Use per capita (m²)',
                                        'Producing or slaughtered animals','Producing or slaughtered animals per capita',
                                        'Imports (t)','imports__tonnes__per_capita','Imports per capita (kg)','Exports (t)',
                                        'exports__tonnes__per_capita','Exports per capita (kg)','Domestic supply (t)',
                                        'domestic_supply__tonnes__per_capita','Domestic supply per capita (kg)','Food (t)',
                                        'food__tonnes__per_capita','Food per capita (kg)','Animal feed (t)',
                                        'feed__tonnes__per_capita','Animal feed per capita (kg)','Other uses (t)',
                                        'other_uses__tonnes__per_capita','Other uses per capita (kg)','Supply chain waste (t)',
                                        'Product','Yield (kg/animal)', 'waste_in_supply_chain__tonnes__per_capita',
                                        'Supply chain waste per capita (kg)', 'Food supply (kg per capita per year)',
                                        'Food supply (g per capita per day)', 'Food supply (Protein g per capita per day)',
                                        'Food supply (Fat g per capita per day)'])

df_obesity.to_csv("df_obesity.csv", index=False)
df_calories.to_csv("df_calories.csv", index=False)