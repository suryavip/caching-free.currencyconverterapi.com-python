# extract list of currencies available
import requests
import json

# getting apikey
with open('apikey.txt', 'r') as apikeyFile:
    apikey = apikeyFile.read()

# getting list of currencies
url = 'https://free.currconv.com/api/v7/currencies?apiKey={}'.format(apikey)
r = requests.get(url)
rj = r.json()
currencies = list(rj['results'].keys())

# storing on currencies.json
with open('currencies.json', 'w') as currenciesFile:
    json.dump(currencies, currenciesFile)