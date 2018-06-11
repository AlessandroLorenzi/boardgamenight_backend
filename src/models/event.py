from db import db
from models.table import TableModel
from datetime import datetime
import string
import secrets

class EventModel(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(80))
    startdate = db.Column(db.DateTime(80))
    enddate = db.Column(db.DateTime(80))
    org = db.Column(db.String(80))
    place = db.Column(db.String(80))

    tables = db.relationship('TableModel', lazy='dynamic')

    def __init__(self, name, startdate, enddate, org, place):
        alphabet = string.ascii_letters + string.digits
        self.id = ''.join(secrets.choice(alphabet) for i in range(10))
        self.set_fields(name, startdate, enddate, org, place)


    def update(self, name, startdate, enddate, org, place):
        self.set_fields(name, startdate, enddate, org, place)

    def set_fields(self, name, startdate, enddate, org, place):
        self.name = name
        timeformat =  "%Y-%m-%d %H:%M:%S"

        self.startdate = datetime.strptime(startdate,timeformat)
        self.enddate = datetime.strptime(enddate,timeformat)
        self.org = org
        self.place = place

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'startdate': str(self.startdate),
            'enddate': str(self.enddate),
            'tables': [table.json() for table in self.tables.all()],
            'place': self.place,
            'org': self.org,
        }
    def reduced_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'startdate': str(self.startdate)
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
