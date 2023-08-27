"""FastAPI dependencies and global variables."""
import mpcor_ai as mai
import mpcor_ai_fastapi as mai_fapi


PRED_MODEL, DEVICE = mai.modeling.utils.load_model(
    mai_fapi.config.SETTINGS.PRED_MODEL_PATH,
    mai_fapi.config.SETTINGS.USE_CUDA,
    mai_fapi.config.SETTINGS.USE_MPS,
)
