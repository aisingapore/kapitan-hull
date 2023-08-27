"""Main module for initialising and defining the FastAPI application."""
import logging
import fastapi
from fastapi.middleware.cors import CORSMiddleware

import mpcor_ai as mai
import mpcor_ai_fastapi as assist_fapi


LOGGER = logging.getLogger(__name__)
LOGGER.info("Setting up logging configuration.")
mai.general_utils.setup_logging(
    logging_config_path=assist_fapi.config.SETTINGS.LOGGER_CONFIG_PATH
)

API_V1_STR = assist_fapi.config.SETTINGS.API_V1_STR
APP = fastapi.FastAPI(
    title=assist_fapi.config.SETTINGS.API_NAME, openapi_url=f"{API_V1_STR}/openapi.json"
)
API_ROUTER = fastapi.APIRouter()
API_ROUTER.include_router(
    assist_fapi.v1.routers.model.ROUTER, prefix="/model", tags=["model"]
)
APP.include_router(API_ROUTER, prefix=assist_fapi.config.SETTINGS.API_V1_STR)

ORIGINS = ["*"]

APP.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
