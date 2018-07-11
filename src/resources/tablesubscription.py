from flask_restful import Resource, reqparse
from models.tablesubscription import TableSubscriptionModel

from flask_jwt_extended import jwt_required, get_jwt_identity

class TableSubscription(Resource):
    @jwt_required
    def post(self, id):
        tablesubscription = TableSubscriptionModel(
            id,
            get_jwt_identity()
        )
        try:
            tablesubscription.save_to_db()
        except:
            return {"message": "An error occurred subscriptioning table."}, 500

        return tablesubscription.json(), 201

    @jwt_required
    def delete(self, id):
        tablesubscription = TableSubscriptionModel.find(id, get_jwt_identity())
        if tablesubscription:
            if tablesubscription.gamer == get_jwt_identity():
                table.delete_from_db()
            else:
                return {'message': 'Not authorized'}, 403
        return {'message': 'Table deleted'}
