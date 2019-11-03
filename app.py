from flask import Flask, request, abort
from flask_restful import Api, Resource
from config import baseCurrency
import time
import json

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


class All(Resource):
    def get(self):
        # return all pair
        try:
            with open('cache_{}.json'.format(baseCurrency), 'r') as currenciesFile:
                currencies = json.load(currenciesFile)
        except:
            abort(404)
        return currencies

class Pair(Resource):
    def get(self, a, b):
        a = a.upper()
        b = b.upper()

        try:
            with open('cache_{}.json'.format(baseCurrency), 'r') as currenciesFile:
                currencies = json.load(currenciesFile)
        except:
            abort(404)

        currencies[baseCurrency] = 1

        if a not in currencies or b not in currencies:
            abort(404)
        
        c = 1 / currencies[a] * currencies[b]
        
        return {'{}-{}'.format(a, b): c}

api.add_resource(All, '/currency')
api.add_resource(Pair, '/currency/<string:a>/<string:b>')

if __name__ == '__main__':
    app.run(debug=True)
