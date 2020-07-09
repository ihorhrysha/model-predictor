from app import db

MODEL_FIELDS = (
    'model_id', 'model_type', 'model_params', 'model', 'transformer'
)


class CurrentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.String(20), index=True)
    model_type = db.Column(db.String(64))
    model_params = db.Column(db.String(140))
    model = db.Column(db.String(2*14))
    transformer = db.Column(db.String(2*14))
    datetime = db.Column(db.DateTime)

    def from_dict(self, data):
        for field in MODEL_FIELDS:
            if field in data:
                setattr(self, field, str(data[field]))

    def __repr__(self):
        return '<Model {} {} from {} with params {}>'.format(
            self.model_id, self.model_type, self.datetime, self.model_params
        )
