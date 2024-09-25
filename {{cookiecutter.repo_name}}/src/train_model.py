"""
This script is for training a dummy model on a dummy dataset.
"""
import os
import logging
import omegaconf
import hydra
import mlflow

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


# pylint: disable = no-value-for-parameter
@hydra.main(version_base=None, config_path="../conf", config_name="train_model.yaml")
def main(args):
    """This is the main function for 'training' the model.
    
    Parameters
    ----------
    args : omegaconf.DictConfig
        An omegaconf.DictConfig object containing arguments for the main function.
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(
        logging_config_path=os.path.join(
            hydra.utils.get_original_cwd(), "conf", "logging.yaml"
        )
    )

    mlflow_init_status, mlflow_run = {{cookiecutter.src_package_name_short}}.general_utils.mlflow_init(
        args, setup_mlflow=args["setup_mlflow"], autolog=args["mlflow_autolog"]
    )
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_params",
        params={
            "dummy_param1": args["dummy_param1"],
            "dummy_param2": args["dummy_param2"],
        },
    )

    model = {{cookiecutter.src_package_name_short}}.modeling.models.DummyModel()

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_dict",
        dictionary=omegaconf.OmegaConf.to_container(args, resolve=True),
        artifact_file="train_model_config.json",
    )

    os.makedirs(args["artifact_dir_path"], exist_ok=True)
    artifact_path = os.path.join(
        args["artifact_dir_path"], "output.txt"
    )
    with open(artifact_path, "w") as f:
        f.write('\n'.join([f'{x}: {args[x]}' for x in args]))
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_artifact",
        local_path=artifact_path,
        artifact_path="outputs"
    )

    if mlflow_init_status:
        artifact_uri = mlflow.get_artifact_uri()
        logger.info("Artifact URI: %s", artifact_uri)
        {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
            mlflow_init_status, "log_params", params={"artifact_uri": artifact_uri}
        )
        logger.info(
            "Model training with MLflow run ID %s has completed.",
            mlflow_run.info.run_id,
        )
        mlflow.end_run()
    else:
        logger.info("Model training has completed.")

    # Outputs for conf/train_model.yaml for hydra.sweeper.direction
    return args["dummy_param1"], args["dummy_param2"]


if __name__ == "__main__":
    main()