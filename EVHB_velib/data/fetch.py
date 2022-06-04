# Fetchs data from opendata.paris
# Retrieves as csv

from time import sleep
import requests
from datetime import datetime
import signal


def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")


def fetch_data():
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M")
    print(current_time)

    url = 'https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
    r = requests.get(url, allow_redirects=True)

    open(f'data/velib/{current_time}_velib.csv', 'wb').write(r.content)


signal.signal(signal.SIGALRM, handler)

for _ in range(1000000):
    try:
        fetch_data()

        now = datetime.now()
        signal.alarm(60 - now.second + 5)
        sleep(60 - now.second + 5)
    except:
        pass
