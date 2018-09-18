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
    image = db.Column(db.String(1024))
    owner = db.Column(db.String(10), db.ForeignKey('gamers.id'))
    tables = db.relationship('TableModel', lazy='dynamic')

    def __init__(self, name, startdate, enddate, org, place, image, owner):
        alphabet = string.ascii_letters + string.digits
        self.id = ''.join(secrets.choice(alphabet) for i in range(10))
        self.set_fields(name, startdate, enddate, org, place, image, owner)


    def update(self, name, startdate, enddate, org, place, image, owner):
        if owner != self.owner:
            raise Exception('unauthorized')
        self.set_fields(name, startdate, enddate, org, place, image, owner)

    def set_fields(self, name, startdate, enddate, org, place, image, owner):

        self.name = name
        timeformat =  "%Y-%m-%d %H:%M:%S"

        self.startdate = datetime.strptime(startdate,timeformat)
        self.enddate = datetime.strptime(enddate,timeformat)
        self.org = org
        self.image = image
        self.place = place
        self.owner = owner


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'startdate': str(self.startdate),
            'enddate': str(self.enddate),
            'tables': [table.json() for table in self.tables.all()],
            'place': self.place,
            'org': self.org,
            'image': self.image,
            'owner': self.owner
        }
    def reduced_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'startdate': str(self.startdate),
            'owner': self.owner,
            'org' : self.org,
            'image' : self.image,
            'ntables' : len(self.tables.all())
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
