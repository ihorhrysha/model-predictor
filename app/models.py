from app import db

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(64))
    active = db.Column(db.Boolean)

    
    def __repr__(self):
        return '<Model {} from {} >'.format(self.name, self.date)    