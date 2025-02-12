"""Module containing definitions and workflows for FastAPI's application endpoints."""

import os
import logging
import fastapi
import pandas as pd

import {{cookiecutter.src_package_name}}_fastapi as {{cookiecutter.src_package_name_short}}_fapi


logger = logging.getLogger(__name__)


ROUTER = fastapi.APIRouter()
PRED_MODEL = {{cookiecutter.src_package_name_short}}_fapi.deps.PRED_MODEL


@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
def predict(csv_file: fastapi.UploadFile):
    """Endpoint that returns the input as-is.

    Args: 
    csv_file : fastapi.UploadFile
        An uploaded CSV file containing the feature columns required by the model.
            Must match the features used during model training.

    Returns:
        FileResponse containing a CSV file with all original columns plus a 
        prediction' column


    Raises:
        HTTPException(400): If the uploaded file is not a CSV file.
        HTTPException(500): If there's an error preventing prediction.
    """
    
    if not csv_file.filename.endswith('.csv'):
        raise fastapi.HTTPException(400, detail="Only CSV files are supported")

    try:
        logger.info("Producing prediction")
        
        contents = csv_file.file.read()
        with open(csv_file.filename, "wb") as buffer:
            buffer.write(contents)
            
        dataframe = pd.read_csv(csv_file.filename)

        predictions = PRED_MODEL.predict(dataframe)
        dataframe['prediction'] = predictions
        
        dataframe.to_csv("./predictions.csv", index=False)

        return fastapi.FileResponse(
                "./predictions.csv",
                media_type="text/csv",
                filename="predictions.csv"
            )

    except Exception as error:
        logger.error(error)
        raise fastapi.HTTPException(status_code=500, detail="Internal server error.")


@ROUTER.get("/version", status_code=fastapi.status.HTTP_200_OK)
def model_version():
    """Get sample version used for the API.

    Returns
    -------
    dict
        Dictionary containing the sample version.
    """
    return {"data": {"model_uuid": {{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.MODEL_UUID}}
