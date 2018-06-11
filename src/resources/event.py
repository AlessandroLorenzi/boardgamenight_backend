from flask_restful import Resource, reqparse
from models.event import EventModel


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

    def post(self, id):
        data = self.parser.parse_args()
        event = EventModel(**data)
        try:
            event.save_to_db()
        except:
            return {"message": "An error occurred creating the event."}, 500

        return event.json(), 201

    def put(self, id):
        data = self.parser.parse_args()

        event = EventModel.find_by_id(id)
        if event:
            event.update(**data)
        else:
            event = EventModel(**data)
        
        try:
            event.save_to_db()
        except:
            return {"message": "An error occurred creating the event."}, 500

        return event.json(), 201

    def delete(self, id):
        event = EventModel.find_by_id(id)
        if event:
            event.delete_from_db()

        return {'message': 'Event deleted'}


class EventList(Resource):
    def get(self):
        return {'events': list(map(lambda x: x.reduced_json(), EventModel.query.all()))}
