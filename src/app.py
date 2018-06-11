#!/usr/bin/env python
import os

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_jwt_identity, create_access_token
)
from resources.event import Event, EventList
from resources.table import Table
from resources.gamer import Gamer


from db import db
from models.gamer import GamerModel

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

api.add_resource(EventList, '/v1/events')
api.add_resource(Event, '/v1/event/<id>')
api.add_resource(Table, '/v1/table/<id>')
api.add_resource(Gamer, '/v1/gamer/<id>')

jwt = JWTManager(app)

@app.route('/auth', methods=['POST'])
def auth():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    gamer = GamerModel.authenticate(username, password)
    if gamer:
        return  jsonify({
            'access_token': create_access_token(identity=gamer.username),
            'refresh_token': create_refresh_token(identity=gamer.username)
        }), 200
    return jsonify({"message": "Unauthorized"}), 403

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return jsonify({
        'access_token': create_access_token(identity=current_user)
    }), 200


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
