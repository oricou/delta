# We needed to find population of each Paris district, so we did.
# tmp is the result for each zone.

from cmath import nan
from enum import unique
import numpy as np
import pandas as pd
import glob
import requests

url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut"


def get_api_url(insee_code):
    return url + f"&q={insee_code}"


def get_postal_code(insee_code):
    print(insee_code)

    url = get_api_url(insee_code)
    res = requests.get(url)
    json = res.json()["records"][0]["fields"]
    return {"population": float(json["population"]) * 1000, "surface": json["superficie"], "postal_code": json["postal_code"]}


unique_arrond = set()
path = "data/velib/grouped_2022_03_10_14_54_velib.csv"
df = pd.read_csv(path, sep=";")

unique_arrond = df["arrond"]
print("fetching postal codes")
# tmp = {insee: get_postal_code(insee) for insee in unique_arrond}
tmp = {75101: {'population': 17600.0, 'surface': 181.0, 'postal_code': '75001'}, 75102: {'population': 22400.0, 'surface': 99.0, 'postal_code': '75002'}, 75103: {'population': 35700.0, 'surface': 116.0, 'postal_code': '75003'}, 75104: {'population': 28200.0, 'surface': 160.0, 'postal_code': '75004'}, 75105: {'population': 61500.0, 'surface': 252.0, 'postal_code': '75005'}, 75106: {'population': 43100.0, 'surface': 215.0, 'postal_code': '75006'}, 75107: {'population': 57400.0, 'surface': 411.0, 'postal_code': '75007'}, 75108: {'population': 40300.0, 'surface': 385.0, 'postal_code': '75008'}, 75109: {'population': 60300.0, 'surface': 218.0, 'postal_code': '75009'}, 75110: {'population': 95900.0, 'surface': 288.0, 'postal_code': '75010'}, 75111: {'population': 152700.0, 'surface': 366.0, 'postal_code': '75011'}, 75112: {'population': 142900.0, 'surface': 1636.0, 'postal_code': '75012'}, 75113: {'population': 182000.0, 'surface': 713.0, 'postal_code': '75013'}, 75114: {'population': 137200.0, 'surface': 560.0, 'postal_code': '75014'}, 75115: {'population': 236500.0, 'surface': 846.0, 'postal_code': '75015'}, 75116: {'population': 169400.0, 'surface': 1641.0, 'postal_code': '75016'}, 75117: {'population': 168500.0, 'surface': 563.0, 'postal_code': '75017'}, 75118: {'population': 200600.0, 'surface': 604.0, 'postal_code': '75018'}, 75119: {'population': 184800.0, 'surface': 674.0, 'postal_code': '75019'}, 75120: {'population': 197100.0, 'surface': 596.0, 'postal_code': '75020'}, 92004: {'population': 81600.0, 'surface': 482.0, 'postal_code': '92600'}, 92007: {'population': 38500.0, 'surface': 418.0, 'postal_code': '92220'}, 92009: {'population': 28200.0, 'surface': 193.0, 'postal_code': '92270'}, 92012: {'population': 113100.0, 'surface': 615.0, 'postal_code': '92100'}, 92014: {'population': 19800.0, 'surface': 186.0, 'postal_code': '92340'}, 92020: {'population': 32400.0, 'surface': 293.0, 'postal_code': '92320'}, 92022: {'population': 18600.0, 'surface': 357.0, 'postal_code': '92370'}, 92023: {'population': 52600.0, 'surface': 876.0, 'postal_code': '92140'}, 92024: {'population': 58200.0, 'surface': 308.0, 'postal_code': '92110'}, 92025: {'population': 84600.0, 'surface': 778.0, 'postal_code': '92700'}, 92026: {'population': 86900.0, 'surface': 416.0, 'postal_code': '92400'}, 92032: {'population': 23700.0, 'surface': 253.0, 'postal_code': '92260'}, 92035: {'population': 27100.0, 'surface': 178.0, 'postal_code': '92250'}, 92036: {'population': 41400.0, 'surface': 1163.0, 'postal_code': '92230'}, 92040: {'population': 64000.0, 'surface': 424.0, 'postal_code': '92130'}, 92044: {'population': 63400.0, 'surface': 241.0, 'postal_code': '92300'}, 92046: {'population': 31000.0, 'surface': 207.0, 'postal_code': '92240'}, 92048: {'population': 44700.0, 'surface': 995.0, 'postal_code': '92190/92360'}, 92049: {'population': 48400.0, 'surface': 207.0, 'postal_code': '92120'}, 92050: {'population': 90000.0, 'surface': 1223.0, 'postal_code': '92000'},
       92051: {'population': 60500.0, 'surface': 371.0, 'postal_code': '92200'}, 92062: {'population': 44900.0, 'surface': 318.0, 'postal_code': '92800'}, 92063: {'population': 79100.0, 'surface': 1453.0, 'postal_code': '92500'}, 92064: {'population': 29700.0, 'surface': 751.0, 'postal_code': '92210'}, 92071: {'population': 19300.0, 'surface': 360.0, 'postal_code': '92330'}, 92072: {'population': 22900.0, 'surface': 392.0, 'postal_code': '92310'}, 92073: {'population': 46100.0, 'surface': 379.0, 'postal_code': '92150'}, 92075: {'population': 26500.0, 'surface': 155.0, 'postal_code': '92170'}, 92077: {'population': 10700.0, 'surface': 369.0, 'postal_code': '92410'}, 93001: {'population': 74700.0, 'surface': 577.0, 'postal_code': '93300'}, 93006: {'population': 33800.0, 'surface': 257.0, 'postal_code': '93170'}, 93008: {'population': 48500.0, 'surface': 674.0, 'postal_code': '93000'}, 93045: {'population': 22400.0, 'surface': 125.0, 'postal_code': '93260'}, 93048: {'population': 103200.0, 'surface': 890.0, 'postal_code': '93100'}, 93053: {'population': 39300.0, 'surface': 503.0, 'postal_code': '93130'}, 93055: {'population': 52200.0, 'surface': 504.0, 'postal_code': '93500'}, 93061: {'population': 18100.0, 'surface': 69.0, 'postal_code': '93310'}, 93063: {'population': 25800.0, 'surface': 345.0, 'postal_code': '93230'}, 93064: {'population': 40900.0, 'surface': 592.0, 'postal_code': '93110'}, 93066: {'population': 105700.0, 'surface': 1238.0, 'postal_code': '93200/93210'}, 93070: {'population': 46500.0, 'surface': 426.0, 'postal_code': '93400'}, 94002: {'population': 44300.0, 'surface': 368.0, 'postal_code': '94140'}, 94003: {'population': 19500.0, 'surface': 232.0, 'postal_code': '94110'}, 94016: {'population': 27800.0, 'surface': 278.0, 'postal_code': '94230'}, 94017: {'population': 75100.0, 'surface': 1130.0, 'postal_code': '94500'}, 94018: {'population': 28800.0, 'surface': 183.0, 'postal_code': '94220'}, 94022: {'population': 39400.0, 'surface': 541.0, 'postal_code': '94600'}, 94033: {'population': 53300.0, 'surface': 557.0, 'postal_code': '94120'}, 94037: {'population': 17500.0, 'surface': 117.0, 'postal_code': '94250'}, 94041: {'population': 57300.0, 'surface': 612.0, 'postal_code': '94200'}, 94042: {'population': 17600.0, 'surface': 227.0, 'postal_code': '94340'}, 94043: {'population': 26400.0, 'surface': 155.0, 'postal_code': '94270'}, 94046: {'population': 52600.0, 'surface': 536.0, 'postal_code': '94700'}, 94052: {'population': 31000.0, 'surface': 279.0, 'postal_code': '94130'}, 94067: {'population': 22600.0, 'surface': 90.0, 'postal_code': '94160'}, 94069: {'population': 14400.0, 'surface': 143.0, 'postal_code': '94410'}, 94076: {'population': 55300.0, 'surface': 528.0, 'postal_code': '94800'}, 94080: {'population': 48700.0, 'surface': 191.0, 'postal_code': '94300'}, 94081: {'population': 85400.0, 'surface': 1165.0, 'postal_code': '94400'}, 95018: {'population': 102800.0, 'surface': 1738.0, 'postal_code': '95100'}}
print("done fetching postal codes")


for path in glob.glob('data/velib/grouped_[0-9]*'):
    print(path)

    data = path.replace("data/velib/grouped_", "data/velib/data_")

    df = pd.read_csv(path, sep=";")
    try:
        df_population = df["arrond"].apply(lambda x: tmp[x]["population"])
        df["ratio_pop"] = df["avail. bike"] / df_population
        df["ratio_pop_log2"] = np.log2(df["ratio_pop"] + 1)
        df["ratio_pop_log10"] = np.log10(df["ratio_pop"] + 1)
        df["ratio_avail"] = df["avail. bike"] / df["capacity"]
        df["ratio_avail_glob"] = df["avail. bike"] / df["capacity"].sum()
        df["ratio_avail_log2"] = np.log2(df["ratio_avail"] + 1)
        df["ratio_avail_log10"] = np.log10(df["ratio_avail"] + 1)
    except:
        print('error', path)
        exit()

    df.to_csv(data, sep=";", index_label=False, index=False)
