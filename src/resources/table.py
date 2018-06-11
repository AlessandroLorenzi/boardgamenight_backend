from flask_restful import Resource, reqparse
from models.table import TableModel


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


    def get(self, id):
        table = EventModel.find_by_id(id)
        if table:
            return event.json()
        return {'message': 'Table not found'}, 404

    def post(self, id):
        data = self.parser.parse_args()
        if len(data['game']) == 0:
            return {"message": "Game empty"}, 400
        table = TableModel(**data)

        try:
            table.save_to_db()
        except:
            return {"message": "An error occurred creating the table."}, 500

        return table.json(), 201

    def delete(self, id):
        table = TableModel.find_by_id(id)
        if table:
            table.delete_from_db()

        return {'message': 'Table deleted'}
