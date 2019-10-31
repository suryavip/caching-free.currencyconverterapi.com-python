# do request and store it in cache
import requests
import json
from config import baseCurrency, numberOfRequests

log = open('create_cache.log', 'a')
log.write('start\n')

# getting apikey
with open('apikey.txt', 'r') as apikeyFile:
    apikey = apikeyFile.read()

# getting list of currencies
with open('currencies.json', 'r') as currenciesFile:
    currencies = json.load(currenciesFile)

# load current cache
try:
    with open('cache_{}.json'.format(baseCurrency), 'r') as cacheFile:
        cache = json.load(cacheFile)
except:
    cache = {}

# load current index position
try:
    with open('index', 'r') as indexFile:
        index = int(indexFile.read())
except:
    index = 0

target = []
while len(target) < numberOfRequests * 2:
    if index >= len(currencies):
        index = 0
    if currencies[index] != baseCurrency:
        target.append(currencies[index])
    index += 1

for x in range(0, numberOfRequests * 2, 2):
    url = 'https://free.currconv.com/api/v7/convert?apiKey={apikey}&q={base}_{target1},{base}_{target2}&compact=ultra'.format(
        apikey=apikey,
        base=baseCurrency,
        target1=target[x],
        target2=target[x+1]
    )
    log.write('getting {} and {}\n'.format(target[x], target[x+1]))
    try:
        r = requests.get(url)
        if r.status_code == 200:
            cur = r.json()
            cache[target[x]] = cur['{}_{}'.format(baseCurrency, target[x])]
            cache[target[x+1]] = cur['{}_{}'.format(baseCurrency, target[x+1])]
    except:
        log.write('failed for {} and {}\n'.format(target[x], target[x+1]))
        pass

# write cache back to file
with open('cache_{}.json'.format(baseCurrency), 'w') as cacheFile:
    json.dump(cache, cacheFile)

# write index position to file
with open('index', 'w') as indexFile:
    indexFile.write('{}'.format(index))

log.write('finish\n')

log.close()