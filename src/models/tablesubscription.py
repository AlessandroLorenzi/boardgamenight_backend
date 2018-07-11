from db import db

class TableSubscriptionModel(db.Model):
    __tablename__ = 'tablesubscriptions'
    gamer = db.Column(db.String(10), db.ForeignKey('gamers.id'), primary_key=True)
    table = db.Column(db.String(10), db.ForeignKey('tables.id'), primary_key=True)

    def __init__(self, table, gamer):
        self.table = table
        self.gamer = gamer

    def json(self):
        return {
            'gamer': self.gamer,
            'table': self.table
        }

    @classmethod
    def find_by_id(cls, table, gamer):
        return cls.query.filter_by(table=table, gamer=gamer).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
