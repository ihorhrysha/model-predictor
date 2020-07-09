from app.rest import api
from flask_restx import Resource, fields
from app.rest.dto import *
from app.rest.service import predict, set_current_model, get_current_model
import pandas as pd


@api.route('/predict')
class Predict(Resource):

    @api.marshal_with(shopping_cart_dto, code=201, description="Blablabla")
    @api.expect(shopping_cart_dto)
    def post(self, **kwargs):
        """
            Make the best prediction ;)
        """
        prediction = predict(api.payload)
        return prediction, 201


@api.route('/current_model')
class CurrentModel(Resource):
    """
       Model that currently in use
    """

    @api.marshal_with(model_info_dto)
    @api.expect(model_input_dto)
    def put(self, **kwargs):
        """
            Change current model
        """
        print(api.payload)
        cur_model = set_current_model(api.payload['modelId'])

        return cur_model, 200

    @api.marshal_with(model_info_dto)
    def get(self, **kwargs):
        """
            Shows model info
        """
        return get_current_model()


@api.route('/feedback')
class Feedback(Resource):

    def post(self, **kwargs):
        return None

    def get(self, **kwargs):
        return None
