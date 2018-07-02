from flask_restful import Resource, reqparse
from models.table import TableModel

from flask_jwt_extended import jwt_required, get_jwt_identity

class Table(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('game',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('event_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )

    @jwt_required
    def post(self, id):
        data = self.parser.parse_args()
        print(data)
        if len(data['game']) == 0:
            return {"message": "Game empty"}, 400
        table = TableModel(
            data.game,
            data.event_id,
            get_jwt_identity()
        )

        try:
            table.save_to_db()
        except:
            return {"message": "An error occurred creating the table."}, 500

        return table.json(), 201

    @jwt_required
    def delete(self, id):
        table = TableModel.find_by_id(id)
        if table:
            if table.owner == get_jwt_identity():
                table.delete_from_db()
            else:
                return {'message': 'Not authorized'}, 403
        return {'message': 'Table deleted'}
