from flask_restx import fields
from app.rest import api

shopping_cart_row_dto = api.model('Shopping Cart Row', {
    'productId': fields.String(example='855109'),
    'quantity': fields.Integer(example='5', default=0),
    'amount': fields.Float(example='20', default=0)
})

shopping_cart_dto = api.model('Shopping Cart', {
    'clientId': fields.String(example='60228'),
    'platformId': fields.String(example='3726012812'),
    'products': fields.List(fields.Nested(model=shopping_cart_row_dto))
})

model_input_dto = api.model('Input Model Data', {
    'modelId': fields.String
})

model_info_dto = api.model('Current Model Info', {
    'modelId': fields.String(attribute='model_id'),
    'modelType': fields.String(attribute='model_type'),
    'modelParams': fields.String(attribute='model_params'),
    'datetime': fields.DateTime
})
