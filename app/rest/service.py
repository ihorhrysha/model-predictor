import os
from os.path import join
from typing import Any, Dict

from flask import current_app
from trainer_app.trainer.data_preprocessor import DataPreprocessor

from app import db
from app.models import CurrentModel
from app.predictor.gbq_connector import BigQueryConnector
from trainer_app.trainer import LRPipeline, NNPipeline, TreePipeline

TARGET_COL = 'UserDiscount'


def predict(shopping_cart):

    # Save cart
    connector = BigQueryConnector()
    shopping_cart_id = connector.save_shopping_cart(shopping_cart)

    # Get DataFrame
    df = connector.get_data(shopping_cart_id)
    print(df.shape)

    # Preprocess
    dp = DataPreprocessor()
    df = dp.preprocess(df, inference=True)

    # Get model and transformer
    model = get_current_model()
    if model is None:
        raise ValueError('Current model is None')
    if model.model_type == 'lr':
        pipeline_cls = LRPipeline
    elif model.model_type == 'nn':
        pipeline_cls = NNPipeline
    elif model.model_type == 'hgbr':
        pipeline_cls = TreePipeline
    else:
        raise ValueError(f'Unknown model type: {model.model_type}')

    model_params = eval(model.model_params)
    pipeline = pipeline_cls(model.model_type, **model_params)
    pipeline.from_serialized_artifacts(
        model_id=model.model_id,
        model_type=model.model_type,
        model_params=model.model_params,
        model=model.model,
        transformer=model.transformer,
        metrics=None
    )

    # Transform
    return_type = get_return_type(model.model_type)
    df = pipeline.transformer.transform(df, return_type=return_type)

    # Run predictions
    pop_column(df, return_type)
    pred = pipeline.model.predict(df)

    # (Optional) Save predictions to DB

    # TODO: save predictions to BQ

    for i, _ in enumerate(shopping_cart['products']):
        shopping_cart['products'][i]['prediction'] = pred[i]
    return shopping_cart


def get_return_type(model_type: str) -> str:
    if model_type == 'nn':
        return 'dict'
    return'df'


def pop_column(df, return_type):
    if return_type == 'df':
        df.pop(TARGET_COL)
    else:
        df.pop(TARGET_COL, None)
    return df


def get_model_filename(file_type, model_id):
    return join(current_app.config["MODELS_PATH"],
                file_type+'_'+str(model_id))


def set_current_model(model_id):

    # Get model data from GBQ
    connector = BigQueryConnector()
    model_data = connector.get_model(model_id)

    print(model_data.keys())

    # Store binaries to file system
    path = get_model_filename('model', model_data['model_id'])
    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)
    write_artifact('model', model_data)
    write_artifact('transformer', model_data)

    # Change new model data to local DB

    current_model = db.session.query(CurrentModel).first()
    if current_model is None:
        current_model = CurrentModel()
        current_model.from_dict(model_data)

    db.session.add(current_model)
    db.session.commit()

    # Delete previous model's files

    return get_current_model()


def write_artifact(name: str, model_data: Dict[str, Any]):
    with open(get_model_filename(name, model_data['model_id']), 'wb') as file:
        file.write(model_data[name])


def get_current_model() -> CurrentModel:
    current_model = db.session.query(CurrentModel).first()
    return current_model
