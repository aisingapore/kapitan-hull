"""Module for containing architectures/definition of models."""
import pandas as pd
import xgboost as xgb
from imblearn.pipeline import Pipeline

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}

class Model:
    """A Model class to train and evaluate an XGBoostRegressor with a predefined pipeline.

    This class builds a pipeline that includes a data preprocessor and an XGBoostRegressor
    for regression tasks.

    Methods:
        train(params, X_train, y_train):
            Fits the pipeline using the provided training data and returns the training score.
        evaluate(X_test, y_test):
            Evaluates the trained model on test data, returning evaluation metrics.
    """

    def __init__(self):
        self.preprocessor = {{cookiecutter.src_package_name_short}}.data_prep.transforms.transformer()

    def train(self, params: dict, X_train: pd.DataFrame, y_train: pd.DataFrame)-> float:
        """Fit an XGBoostRegressor through a pipeline with predefined steps.

        Args:
        params (dict): Dictionary with parameters to train the model.
        X_train (pandas.DataFrame): The training input samples as a pandas DataFrame.
        y_train (pandas.DataFrame): The target values as a pandas DataFrame.

        Returns:
            float: The score from XGBoostRegressor.score() on the training dataset
        """
        self.steps = [
            ("preprocessor", self.preprocessor),
            ("XGBR", xgb.XGBRegressor(**params)),
        ]
        self.pipeline = Pipeline(self.steps)

        self.pipeline.fit(X_train, y_train)
        self.y_train_pred = self.pipeline.predict(X_train)
        self.train_score = self.pipeline.score(X_train, y_train)

        return self.train_score

    def evaluate(self, X_test, y_test):
        ## Create your own evaluation function
        pass
