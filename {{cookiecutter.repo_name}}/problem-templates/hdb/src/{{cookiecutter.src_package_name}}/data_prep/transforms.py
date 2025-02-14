"""Definition of transforms sequence for data preparation."""

from typing import Tuple

import numpy as np
import pandas as pd
from category_encoders import BinaryEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder


class Transform:
    def __init__(self):
        """
        Initialize the Transform object
        """
        pass

    def clean_data(self, raw_data: pd.DataFrame):
        ## Placeholder function, change accordingly
        return raw_data

    def split_data(
        self, cleaned_data: pd.DataFrame, test_size: float, seed: int
    ) -> Tuple[pd.DataFrame]:
        # Define X as input features and y as the outcome variable
        X = cleaned_data.drop(["resale_price"], axis=1).copy()
        y = cleaned_data["resale_price"].copy()

        # Test/train split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=seed
        )
        return X_train, X_test, y_train, y_test

    def transformer(
        self, num_cols: list, cat_cols: list, ord_cols: list, ord_order: list
    ) -> ColumnTransformer:
        """
        EXAMPLE:
        Creates a column transformer with predefined transformers for the
        specified columns.

        This method sets up a ColumnTransformer that applies:
          - A logarithmic transformation (`np.log1p`) to numerical columns.
          - Binary encoding to categorical columns.
          - Ordinal encoding to ordinal columns based on the specified order.

        Args:
            num_cols (list): List of numerical column names.
            cat_cols (list): List of categorical column names.
            ord_cols (list): List of ordinal column names.
            ord_order (list): List specifying the order of categories for
                ordinal encoding.

        Returns:
            ColumnTransformer: A user-defined ColumnTransformer object containing
                a series of transformers that will be applied to the designated
                columns when used in a scikit-learn pipeline.
        """

        log_transformer = FunctionTransformer(np.log1p, feature_names_out="one-to-one")

        preprocessor = ColumnTransformer(
            transformers=[
                ("log", log_transformer, num_cols),
                ("bin_enc", BinaryEncoder(), cat_cols),
                (
                    "ord_enc",
                    OrdinalEncoder(categories=[ord_order]),
                    ord_cols,
                ),
            ],
            remainder="passthrough",
            sparse_threshold=0,
        )
        return preprocessor

    def transform(
        self, input_data: pd.DataFrame, test_size: float, seed: int
    ) -> Tuple[pd.DataFrame]:
        df_clean = self.clean_data(input_data)
        X_train, X_test, y_train, y_test = self.split_data(df_clean, test_size, seed)

        return X_train, X_test, y_train, y_test

    ## Create any other transformation functions that you need in the Transform class
