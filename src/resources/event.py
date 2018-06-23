from flask_restful import Resource, reqparse
from models.event import EventModel

from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('startdate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('enddate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('org',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('place',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    def get(self, id):
        event = EventModel.find_by_id(id)
        if event:
            return event.json()
        return {'message': 'Event not found'}, 404

    @jwt_required
    def post(self, id):
        data = self.parser.parse_args()
        event = EventModel(
            data.name,
            data.startdate,
            data.enddate,
            data.org,
            data.place,
            get_jwt_identity()
        )
        try:
            event.save_to_db()
        except:
            return {"message": "An error occurred creating the event."}, 500

        return event.json(), 201

    @jwt_required
    def put(self, id):
        data = self.parser.parse_args()

        event = EventModel.find_by_id(id)
        if event:
            try:
                event.update(
                    data.name,
                    data.startdate,
                    data.enddate,
                    data.org,
                    data.place,
                    get_jwt_identity()
                )
            except:
                return {"message": "Non autorizzato"}, 403
        else:
            event = EventModel(
                data.name,
                data.startdate,
                data.enddate,
                data.org,
                data.place,
                get_jwt_identity()
            )
        try:
            event.save_to_db()
        except:
            return {"message": "An error occurred creating the event."}, 500

        return event.json(), 201

    @jwt_required
    def delete(self, id):
        event = EventModel.find_by_id(id)
        if event:
            if event.owner == get_jwt_identity():
                event.delete_from_db()
            else:
                return {'message': 'Non autorizzato'}, 403

        return {'message': 'Event deleted'}


class EventList(Resource):
    def get(self):
        return {'events': list(map(lambda x: x.reduced_json(), EventModel.query.all()))}
