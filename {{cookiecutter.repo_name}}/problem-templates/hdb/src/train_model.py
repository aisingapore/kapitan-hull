"""
This script is for training a XGBRegressor model on the HDB dataset.
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
    
    params = {
        "n_estimators": args["n_estimators"],
        "learning_rate": args["lr"],
        "gamma": args["gamma"],
        "max_depth": args["max_depth"],
    }
     
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_params",
        params=params,
    )

    model = {{cookiecutter.src_package_name_short}}.modeling.models.Model()
    
    ### Insert your model code
    # train_score = model.train(params, X_train, y_train, mlflow_init_status)
    # test_rmse = model.evaluate()
    

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_dict",
        dictionary=omegaconf.OmegaConf.to_container(args, resolve=True),
        artifact_file="train_model_config.json",
    )

    os.makedirs(args["artifact_dir_path"], exist_ok=True)
    artifact_path = os.path.join(
        args["artifact_dir_path"], "xgbreg.json"
    )
    
    # model.save_model(os.path.join(args["artifact_dir_path"], "xgbreg.json"))
    
    with open(artifact_path, "w") as f:
        f.write('\n'.join([f'{x}: {args[x]}' for x in args]))
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_artifact",
        local_path=artifact_path,
        artifact_path="model"
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

    ## Uncomment return line
    ## The function decorated with @hydra.main() returns a value that we want to
    ## adjust base on hydra.sweeper.direction in conf/train_model.yaml
    # return test_rmse


if __name__ == "__main__":
    main()