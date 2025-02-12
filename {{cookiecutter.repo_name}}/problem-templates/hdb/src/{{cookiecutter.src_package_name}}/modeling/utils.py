"""Utilities for model training and experimentation workflows.
"""
import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}
import xgboost as xgb


def load_model(path_to_model: str, use_cuda: bool) -> xgb.XGBRegressor:
    """Load trained model.
    In this example, we are using XGBoost, modify this method to suit your
    models.

    Returns
    -------
    loaded_model : 
        Object containing loaded model.
    """
    loaded_model = xgb.XGBRegressor()
    loaded_model.load_model(path_to_model)
    if use_cuda:
        loaded_model.set_params(device="cuda", tree_method="hist")

    return loaded_model