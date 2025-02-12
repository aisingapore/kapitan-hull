"""Utilities for model training and experimentation workflows.
"""
import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


def load_model(path_to_model: str):
    """Load dummy model.

    A sample utility function to be used.

    Returns
    -------
    loaded_model : 
        Object containing dummy model.
    """
    loaded_model = {{cookiecutter.src_package_name_short}}.modeling.models.Model()

    return loaded_model