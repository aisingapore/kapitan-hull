"""Configuration module for the FastAPI application."""
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Settings for the FastAPI application."""

    API_NAME: str = "{{cookiecutter.project_name}} - Fastapi"
    API_V1_STR: str = "/api/v1"
    LOGGER_CONFIG_PATH: str = "../conf/logging.yaml"

    USE_CUDA: bool = False
    USE_MPS: bool = False
    PRED_MODEL_UUID: str = "test"
    PRED_MODEL_PATH: str


SETTINGS = Settings()
