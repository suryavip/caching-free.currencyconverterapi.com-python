# Caching free.currencyconverterapi.com
Periodically send request to https://free.currencyconverterapi.com without exceeding "Requests per Hour" limit and cache the result. Useful for application that don't need realtime and accurate conversion rate.

# Setup
1. Fullfill the pip requirements by doing:
	>`pip install -r requirements.txt`
1. Make sure you have your own API key from https://free.currencyconverterapi.com
1. Put your API key into `apikey.txt` file
1. Adjust your `baseCurrency` in `config.py`
1. Adjust your `numberOfRequests` in `config.py`. This will control how much request to be sent every time `create_cache.py` run. For example, if I set a cron job to run `create_cache.py` every 5 minutes, there will be 72 request sent in 1 hour (60 minutes / 5 minutes * 6 requests) which is still below the 100 requests per hour limit. Since each request will ask for 2 pairs of currency, 144 pairs will be updated each time `create_cache.py` run.
1. Run `update_currencies.py` to get all currencies offered by https://free.currencyconverterapi.com. You can remove currencies that you don't need from `currencies.json`.

# Usage
Run `create_cache.py` periodically (use script or cron job). In my case, I run it once every 5 minutes. Run `app.py` to start the Flask server (or use passenger) to serve the cached result:
1. `GET currency` will return all cached currencies
1. `GET curerncy/XXX/YYY` will return the rate for XXX and YYY pair.
