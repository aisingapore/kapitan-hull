"""FastAPI dependencies and global variables."""
import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}
import {{cookiecutter.src_package_name}}_fastapi as {{cookiecutter.src_package_name_short}}_fapi

PRED_MODEL  = {{cookiecutter.src_package_name_short}}.modeling.utils.load_model()