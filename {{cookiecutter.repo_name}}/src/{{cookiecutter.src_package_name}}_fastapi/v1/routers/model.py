"""Module containing definitions and workflows for FastAPI's application endpoints."""
import os
import logging
import fastapi

import {{cookiecutter.src_package_name}}_fastapi as {{cookiecutter.src_package_name_short}}_fapi


logger = logging.getLogger(__name__)


ROUTER = fastapi.APIRouter()
PRED_MODEL = {{cookiecutter.src_package_name_short}}_fapi.deps.PRED_MODEL


@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
def predict(data: str):
    """Endpoint that returns the input as-is.

    Parameters
    ----------
    data : str
        Input text.

    Returns
    -------
    result_dict : dict
        Dictionary containing the input string.
    
    Raises
    ------
    fastapi.HTTPException
        A 500 status error is returned if the prediction steps
        encounters any errors.
    """
    result_dict = {"data": []}

    try:
        logger.info("Copying input...")

        pred_str = PRED_MODEL.predict(data)

        result_dict["data"].append(
            "input": pred_str
        )
        logger.info("Input: %s", data)

    except Exception as error:
        logger.error(error)
        raise fastapi.HTTPException(status_code=500, detail="Internal server error.")
    
    return result_dict

@ROUTER.get("/version", status_code=fastapi.status.HTTP_200_OK)
def model_version():
    """Get sample version used for the API.

    Returns
    -------
    dict
        Dictionary containing the sample version.
    """
    return {"data": {"model_uuid": {{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.MODEL_UUID}}