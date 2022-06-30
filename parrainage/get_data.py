import requests

def fetch_data():
    url = "https://static.data.gouv.fr/resources/parrainages-des-candidats-a-lelection-presidentielle-francaise-de-2022/20220307-183308/parrainagestotal.csv"
    req = requests.get(url, allow_redirects=True)
    csv_file = open('NC_FM_parrainage/data/parrainagestotal.csv', 'wb')
    csv_file.write(req.content)
    csv_file.close()

    url_geojson = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    req = requests.get(url_geojson, allow_redirects=True)
    csv_file = open('NC_FM_parrainage/data/departements.geojson', 'wb')
    csv_file.write(req.content)
    csv_file.close()
