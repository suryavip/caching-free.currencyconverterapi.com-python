# extract list of currencies available

from config import Config
import requests

url = 'https://free.currconv.com/api/v7/currencies?apiKey={}'.format(Config.apikey)
r = requests.get(url)
rj = r.json()
currencies = list(rj['results'].keys())

print(currencies)