from flask import Flask, request
from flask_restful import Api, Resource
from config import Config
from connection import MysqlCon
from datetime import datetime, date
import requests
import math
import time

app = Flask(__name__, static_url_path='')
api = Api(app)

@app.after_request
def after_request(response):
    requesterOrigin = request.environ.get('HTTP_ORIGIN')
    response.headers["Access-Control-Allow-Origin"] = requesterOrigin
    response.headers["Access-Control-Allow-Headers"] = "Accept, Accept-Language, Content-Language, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    # I use this piece of code because on server where I host, somehow it will return 404 if there is consecutive requests within 1 second. Since CORS request will be OPTIONS + GET, I give 1 second delay for the OPTIONS request
    requestMethod = request.environ.get('REQUEST_METHOD')
    if requestMethod == 'OPTIONS':
        time.sleep(1)

    return response


class Currency(Resource):
    def get(self):
        # return all pair
        mysqlCon = MysqlCon()
        result = mysqlCon.rQuery('SELECT currencyId, currencyValue FROM currency')
        cur = {}
        for (currencyId, currencyValue) in result:
            cur[currencyId] = str(currencyValue)
        return cur

    def post(self):
        # requesting and store cache
        t = datetime.now().time()
        h = t.hour
        m = t.minute
        if h >= 12: h -= 12
        i = (h * 12) + math.floor(m / 5) #12 times per hour (every 5 min)
        i *= 2 #because do 2 currencies at one shot

        if i >= len(Config.currencies):
            return {}

        dt = date.today().isoformat()
        ca = Config.currencies[i]
        cb = Config.currencies[i + 1]

        url = 'https://free.currconv.com/api/v7/convert?apiKey={apikey}&q={base}_{target1},{base}_{target2}&compact=ultra'.format(
            apikey=Config.apikey,
            base=Config.baseCurrency,
            target1=ca,
            target2=cb
        )
       
        r = requests.get(url)
        if r.status_code == 200:
            cur = r.json()
            try:
                va = cur['EUR_{}'.format(ca)][dt]
                vb = cur['EUR_{}'.format(cb)][dt]
                #store va vb
            except:
                pass

        return {}


api.add_resource(Currency, '/currency')

if __name__ == '__main__':
    app.run(debug=True)
