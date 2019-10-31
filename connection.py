from flask_restful import abort
from privateConfig import PrivateConfig
import mysql.connector


class MysqlCon:
    def __init__(self):
        self.db = mysql.connector.connect(**PrivateConfig.mysql)
        self.cursor = self.db.cursor()
        self.Error = mysql.connector.Error

    def rQuery(self, query, param=(), errorHandler={}):
        try:
            self.cursor.execute((query), param)
        except self.Error as err:
            if '{}'.format(err.errno) in errorHandler:
                thisError = errorHandler['{}'.format(err.errno)]
                abort(thisError['httpCode'], code=thisError['code'])
            abort(400, code='{}'.format(err.errno), msg={
                'query': query,
                'param': param,
            })
        result = self.cursor.fetchall()
        return result

    def wQuery(self, query, param=(), errorHandler={}):
        try:
            self.cursor.execute((query), param)
        except self.Error as err:
            if '{}'.format(err.errno) in errorHandler:
                thisError = errorHandler['{}'.format(err.errno)]
                abort(thisError['httpCode'], code=thisError['code'])
            abort(400, code='{}'.format(err.errno), msg={
                'query': query,
                'param': param,
            })

    def insertQuery(self, tableName, data, updateOnDuplicate=False, errorHandler={}):
        cols = data[0].keys()

        colsN = ','.join(cols)

        colsQ = ['%s'] * len(cols)
        colsQ = ','.join(colsQ)

        valsQ = ['({})'.format(colsQ)] * len(data)
        valsQ = ','.join(valsQ)

        vals = []
        for r in data:
            for c in r:
                vals.append(r[c])

        query = "INSERT INTO {} ({}) VALUES {}".format(tableName, colsN, valsQ)
        if updateOnDuplicate == True:
            dupQ = ['{} = VALUES({})'.format(c, c) for c in cols]
            dupQ = ','.join(dupQ)
            query = "INSERT INTO {} ({}) VALUES {} ON DUPLICATE KEY UPDATE {}".format(tableName, colsN, valsQ, dupQ)

        return self.wQuery(
            query,
            tuple(vals),
            errorHandler
        )
