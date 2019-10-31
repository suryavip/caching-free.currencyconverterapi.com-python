# do request and store it in cache
import requests
import json
from datetime import datetime
import os

# getting apikey
with open('apikey.txt', 'r') as apikeyFile:
    apikey = apikeyFile.read()

# getting list of currencies
with open('currencies.json', 'r') as currenciesFile:
    currencies = json.load(currenciesFile)

baseCurrency = 'EUR' # you can change this
numberOfRequests = 6 # 2 pairs per requests. 6 requests means 12 pairs

with open('last_index', 'r') as lastIndexFile:
    lastIndex = int(lastIndexFile.read())