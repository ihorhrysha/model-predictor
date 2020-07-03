
from app.predictor.gbq_connector import BigQueryConnector
from flask import current_app
from os.path import join
from app import db
from app.models import CurrentModel


def predict(shopping_cart):

    # Save cart
    connector = BigQueryConnector()
    shopping_cart_id = connector.save_shopping_cart(shopping_cart)

    # Get DataFrame
    df = connector.get_data(shopping_cart_id)
    print(df.shape)
    # Transform

    # Run predictions

    # (Optional) Save predictions to DB

    return shopping_cart_id


def get_model_filename(file_type, model_id):
    return join(current_app.config["MODELS_PATH"],
                file_type+'_'+str(model_id))


def set_current_model(model_id):

    # Get model data from GBQ
    connector = BigQueryConnector()
    model_data = connector.get_model(model_id)

    print(model_data.keys())

    # Store binaries to file system
    with open(get_model_filename('model', model_data['model_id']), 'wb') as file:
        file.write(model_data['model'])

    with open(get_model_filename('transformer', model_data['model_id']), 'wb') as file:
        file.write(model_data['transformer'])

    # Change new model data to local DB

    current_model = db.session.query(CurrentModel).first()
    if current_model is None:
        current_model = CurrentModel()
        current_model.from_dict(model_data)

    db.session.add(current_model)
    db.session.commit()

    # Delete previous model's files

    return get_current_model()


def get_current_model():
    current_model = db.session.query(CurrentModel).first()
    return current_model
