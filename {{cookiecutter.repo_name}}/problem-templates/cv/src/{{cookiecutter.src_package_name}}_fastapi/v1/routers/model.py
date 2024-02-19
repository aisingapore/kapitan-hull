"""Module containing definitions and workflows for FastAPI's application endpoints."""
import os
import logging
import fastapi
import torchvision
from PIL import Image

import {{cookiecutter.src_package_name}}_fastapi as {{cookiecutter.src_package_name_short}}_fapi


logger = logging.getLogger(__name__)


ROUTER = fastapi.APIRouter()
PRED_MODEL = {{cookiecutter.src_package_name_short}}_fapi.deps.PRED_MODEL
DEVICE = {{cookiecutter.src_package_name_short}}_fapi.deps.DEVICE


@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
def classify_image(image_file: fastapi.UploadFile):
    """Endpoint that returns sentiment classification of movie review
    texts.

    Parameters
    ----------
    image_file : fastapi.UploadFile
        'fastapi.UploadFile' object.

    Returns
    -------
    dict
        Dictionary containing the file name and prediction for the image.

    Raises
    ------
    fastapi.HTTPException
        A 500 status error is returned if the prediction steps
        encounters any errors.
    """
    result_dict = {"data": []}

    try:
        logger.info("Classifying image...")

        contents = image_file.file.read()
        with open(image_file.filename, "wb") as buffer:
            buffer.write(contents)
        image = Image.open(image_file.filename)
        image = torchvision.transforms.functional.to_grayscale(image)
        image = torchvision.transforms.functional.to_tensor(image)
        output = PRED_MODEL(image.unsqueeze(0).to(DEVICE))
        pred = output.argmax(dim=1, keepdim=True)
        pred_str = str(int(pred[0]))

        result_dict["data"].append(
            {"image_filename": image_file.filename, "prediction": pred_str}
        )
        logger.info(
            "Prediction for image filename %s: %s", image_file.filename, pred_str
        )

    except Exception as error:
        print(error)
        raise fastapi.HTTPException(status_code=500, detail="Internal server error.")

    finally:
        image_file.file.close()
        os.remove(image_file.filename)

    return result_dict


@ROUTER.get("/version", status_code=fastapi.status.HTTP_200_OK)
def get_model_version():
    """Get version (UUID) of predictive model used for the API.

    Returns
    -------
    dict
        Dictionary containing the UUID of the predictive model being
        served.
    """
    return {"data": {"model_uuid": {{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.PRED_MODEL_UUID}}
