from flask_restful import Resource, reqparse
from models.gamer import GamerModel


class Gamer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('email',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    def get(self, id):
        gamer = GamerModel.find_by_id(id)
        if gamer:
            return gamer.json()
        return {'message': 'Gamer not found'}, 404
        
    def find(self, name):
        gamer = GamerModel.find_by_username(name)
        if gamer:
            return gamer.json()
        return {'message': 'Gamer not found'}, 404


    def post(self, id):
        data = self.parser.parse_args()
        gamer = GamerModel(**data)
        self.save(gamer)

    def put(self, id):
        data = self.parser.parse_args()
        gamer = GamerModel.find_by_name(data['name'])
        if gamer:
            gamer.update(**data)
        else:
            gamer = GamerModel(**data)
        return self.save(gamer)

    def save(self, gamer):
        try:
            gamer.save_to_db()
        except:
            return {'message': 'Impossibile salvare'}, 500
        return gamer.json(), 201
