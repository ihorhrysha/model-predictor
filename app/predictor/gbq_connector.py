from google.cloud import bigquery
from google.oauth2 import service_account
from flask import current_app
import pickle as pkl
from datetime import datetime
from .utils import read_sql_query
import uuid
from os.path import dirname, abspath, join


class BigQueryConnector:
    def __init__(self, key_path=None):
        credentials = service_account.Credentials.from_service_account_file(
            (current_app.config["GOOGLE_APPLICATION_CREDENTIALS"] or key_path),
            scopes=["https://www.googleapis.com/auth/cloud-platform",
                    'https://www.googleapis.com/auth/drive'],
        )

        self.client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )

    def get_data(self, shopping_cart_id):

        query_path = join(abspath(dirname(__file__)),
                          'get_predict_data.sql')

        query_string = read_sql_query(query_path)
        return self.query(query_string.format(shopping_cart_id))

    def query(self, select):
        return self.client.query(select).to_dataframe()

    def save_shopping_cart(self, shopping_cart):
        shopping_cart_id = str(uuid.uuid1())

        table = self.client.get_table('prosteer.ShoppingCarts')
        rows_to_insert = []

        for shopping_cart_product in shopping_cart['products']:
            rows_to_insert.append((
                shopping_cart_id,
                datetime.now(),
                shopping_cart['platformId'],
                shopping_cart['clientId'],
                shopping_cart_product['productId'],
                shopping_cart_product['quantity'],
                shopping_cart_product['amount']
            ))
        errors = self.client.insert_rows(table, rows_to_insert)
        if errors:
            raise RuntimeError(
                'An error occurred while saving model to BigQuery')

        return shopping_cart_id

    def get_model(self, model_id):

        result = self.query(
            'SELECT * FROM models.Models as m WHERE m.model_id = "{}" LIMIT 1'.format(model_id))

        if result.empty:
            raise RuntimeError("Invalid Model Id {}".format(model_id))

        model_data = result.iloc[0].to_dict()

        return model_data
