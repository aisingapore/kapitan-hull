"""
This script is for training a dummy model on a dummy dataset.
"""
import os
import logging
import json
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
        ),
        log_dir=args.get("log_dir", None)
    )
    logger.info(
        "Starting training with {} epochs, lr={}, batch_size={}".format(
            args['epochs'], args['lr'], args['train_bs']
        )
    )

    mlflow_init_status, mlflow_run, step_offset = {{cookiecutter.src_package_name_short}}.general_utils.mlflow_init(
        args["mlflow_tracking_uri"], args["mlflow_exp_name"], 
        args["mlflow_run_name"], setup_mlflow=args["setup_mlflow"], 
        autolog=args["mlflow_autolog"], resume=args["resume"]
    )
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_params",
        params={
            "learning_rate": args["lr"],
            "train_batch_size": args["train_bs"],
            "test_batch_size": args["test_bs"]
        },
    )

    dataset = {{cookiecutter.src_package_name_short}}.data_prep.datasets.DummyDataset(args["data_dir_path"])

    model = {{cookiecutter.src_package_name_short}}.modeling.models.DummyModel()
    
    for epoch in range(step_offset + 1, args["epochs"] + step_offset + 1):
        curr_train_loss = {{cookiecutter.src_package_name_short}}.modeling.utils.train(
            mlflow_init_status, model, dataset, epoch, 
            learning_rate=args["lr"],
            batch_size=int(args["train_bs"])
        )
        curr_test_loss, curr_test_accuracy = {{cookiecutter.src_package_name_short}}.modeling.utils.test(
            mlflow_init_status, model, dataset, epoch,
            test_size=args["test_bs"]
        )

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_dict",
        dictionary=omegaconf.OmegaConf.to_container(args, resolve=True),
        artifact_file="train_model_config.json",
    )

    # Save metrics to artifact directory
    os.makedirs(args["artifact_dir_path"], exist_ok=True)
    
    # Save training configuration
    artifact_path = os.path.join(
        args["artifact_dir_path"], "output.txt"
    )
    with open(artifact_path, "w") as f:
        f.write('\n'.join([f'{x}: {args[x]}' for x in args]))
    
    # Log artifacts to MLflow
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
    return curr_test_loss, curr_test_accuracy


if __name__ == "__main__":
    main()
