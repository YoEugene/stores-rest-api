from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) # limit the size of username to 80
    price = db.Column(db.Float(precision=2)) # limit the size of username to 40

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel') # a single object of store!

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # same as: SELECT * FROM items WHRER name=:name LIMIT 1

    def save_to_db(self): # include update and insert --> upserting!
        db.session.add(self) # the collection of objects that we're going to write into db
        db.session.commit() # commit the write

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
