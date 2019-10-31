from flask_restful import Resource, reqparse, abort
from connection import FirebaseCon, MysqlCon

# NO NEED FOR EXTENSIVE DATA VALIDATION. VALIDATE ONLY WHAT DANGEROUS FOR SERVER AND OTHER DATA

class Wallet(Resource):
    def post(self):
        mysqlCon = MysqlCon()
        parser = reqparse.RequestParser()
        parser.add_argument('X-idToken', required=True, type=str, help='a', location='headers')
        parser.add_argument('X-timestamp', required=True, type=int, location='headers')
        parser.add_argument('walletId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('currency', required=True)
        args = parser.parse_args()

        fbc = FirebaseCon(args['X-idToken'])

        # store data
        mysqlCon.insertQuery('walletdata', [{
            'walletId': args['walletId'],
            'ownerUserId': fbc.uid,
            'name': args['name'],
            'currency': args['currency'],
        }], updateOnDuplicate=True)

        if mysqlCon.cursor.rowcount == 0:
            return self.get()

        fbc.updateRDBTimestamp(args['X-timestamp'], ['poke/{}/wallet'.format(fbc.uid)])

        mysqlCon.db.commit()

        return self.get()

    def delete(self):
        mysqlCon = MysqlCon()
        parser = reqparse.RequestParser()
        parser.add_argument('X-idToken', required=True, type=str, help='a', location='headers')
        parser.add_argument('X-timestamp', required=True, type=int, location='headers')
        parser.add_argument('walletId', required=True)
        args = parser.parse_args()

        fbc = FirebaseCon(args['X-idToken'])

        walletCount = mysqlCon.rQuery(
            'SELECT COUNT(walletId) AS c FROM walletdata WHERE ownerUserId = %s',
            (fbc.uid,)
        )
        for (c,) in walletCount:
            if c <= 1:
                return self.get()

        # store data
        mysqlCon.wQuery(
            'DELETE FROM walletdata WHERE walletId = %s AND ownerUserId = %s',
            (args['walletId'], fbc.uid)
        )

        fbc.updateRDBTimestamp(args['X-timestamp'], ['poke/{}/wallet'.format(fbc.uid)])

        mysqlCon.db.commit()

        return self.get()

    def get(self):
        mysqlCon = MysqlCon()
        parser = reqparse.RequestParser()
        parser.add_argument('X-idToken', required=True, type=str, help='a', location='headers')
        args = parser.parse_args()

        fbc = FirebaseCon(args['X-idToken'])

        wallet = mysqlCon.rQuery(
            'SELECT walletId, name, currency FROM walletdata WHERE ownerUserId = %s',
            (fbc.uid,)
        )

        return {
            'channel': 'wallet',
            'data': [{
                'walletId': walletId,
                'name': name,
                'currency': currency,
            } for (walletId, name, currency) in wallet],
        }