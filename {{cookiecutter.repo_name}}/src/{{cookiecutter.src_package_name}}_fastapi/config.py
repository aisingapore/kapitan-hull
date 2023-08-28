"""Configuration module for the FastAPI application."""
import pydantic


class Settings(pydantic.BaseSettings):
    """Settings for the FastAPI application."""

    API_NAME: str = "{{cookiecutter.project_name}} - Fastapi"
    API_V1_STR: str = "/api/v1"
    LOGGER_CONFIG_PATH: str = "../conf/base/logging.yaml"

    USE_CUDA: bool = False
    USE_MPS: bool = False
    PRED_MODEL_UUID: str
    PRED_MODEL_PATH: str


SETTINGS = Settings()
