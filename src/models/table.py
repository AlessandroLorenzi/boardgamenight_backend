from db import db
import string
import secrets
from models.tablesubscription import TableSubscriptionModel


class TableModel(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.String(10), primary_key=True)
    game = db.Column(db.String(80))
    event_id = db.Column(db.String(10), db.ForeignKey('events.id'))
    owner = db.Column(db.String(10), db.ForeignKey('gamers.id'))

    tablesubscribtions = db.relationship('TableSubscriptionModel', lazy='dynamic')

    def __init__(self, game, event_id, owner):
        alphabet = string.ascii_letters + string.digits
        self.id = ''.join(secrets.choice(alphabet) for i in range(10))
        self.game = game
        self.event_id = event_id
        self.owner = owner

    def json(self):
    
        return {
            'id': self.id,
            'event_id': self.event_id,
            'game': self.game,
            'owner': self.owner,
            'tablesubscribtions': [
                tablesubscribtions.json() for tablesubscribtions in self.tablesubscribtions.all()
            ],
        }


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
