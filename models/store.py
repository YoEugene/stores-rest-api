from db import db

class StoreModel(db.Model):
    # tell sqlalchemy the table name
    __tablename__ = 'stores'

    # tell sqlalchemy the column names, same as attributes in __init__
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) # limit the size of username to 80

    items = db.relationship('ItemModel', lazy='dynamic') # list of item objects!

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # same as: SELECT * FROM items WHRER name=:name LIMIT 1

    def save_to_db(self): # include update and insert --> upserting!
        db.session.add(self) # the collection of objects that we're going to write into db
        db.session.commit() # commit the write

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
