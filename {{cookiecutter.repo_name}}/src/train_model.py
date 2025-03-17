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
        )
    )

    mlflow_init_status, mlflow_run = {{cookiecutter.src_package_name_short}}.general_utils.mlflow_init(
        args["mlflow_tracking_uri"], args["mlflow_exp_name"], 
        args["mlflow_run_name"], setup_mlflow=args["setup_mlflow"], 
        autolog=args["mlflow_autolog"], resume=args["resume"]
    )
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_params",
        params={
            "dummy_param1": args["dummy_param1"],
            "dummy_param2": args["dummy_param2"],
        },
    )

    # Create model
    model = {{cookiecutter.src_package_name_short}}.modeling.models.DummyModel()
    
    # Train the model
    logger.info("Starting model training...")
    epochs = 5  # Default number of epochs
    train_metrics = {{cookiecutter.src_package_name_short}}.modeling.utils.train(
        model, 
        epochs=epochs, 
        learning_rate=args["dummy_param1"],
        batch_size=int(32 * args["dummy_param2"])
    )
    
    # Test the model
    logger.info("Evaluating model...")
    test_metrics = {{cookiecutter.src_package_name_short}}.modeling.utils.test(model)
    
    # Log metrics to MLflow
    if mlflow_init_status:
        # Log final metrics
        mlflow.log_metric("final_train_loss", train_metrics["train_loss"][-1])
        mlflow.log_metric("final_train_accuracy", train_metrics["train_accuracy"][-1])
        mlflow.log_metric("test_loss", test_metrics["test_loss"])
        mlflow.log_metric("test_accuracy", test_metrics["test_accuracy"])
        
        # Log metrics for each epoch
        for epoch, (loss, acc) in enumerate(zip(train_metrics["train_loss"], 
                                               train_metrics["train_accuracy"]), 1):
            mlflow.log_metric("train_loss", loss, step=epoch)
            mlflow.log_metric("train_accuracy", acc, step=epoch)

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_dict",
        dictionary=omegaconf.OmegaConf.to_container(args, resolve=True),
        artifact_file="train_model_config.json",
    )

    # Save metrics to artifact directory
    os.makedirs(args["artifact_dir_path"], exist_ok=True)
    
    # Save training configuration
    artifact_path = os.path.join(args["artifact_dir_path"], "output.txt")
    with open(artifact_path, "w") as f:
        f.write('\n'.join([f'{x}: {args[x]}' for x in args]))
    
    # Save metrics
    metrics_path = os.path.join(args["artifact_dir_path"], "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump({
            "training": train_metrics,
            "testing": test_metrics,
            "hyperparameters": {
                "learning_rate": args["dummy_param1"],
                "batch_size_factor": args["dummy_param2"]
            }
        }, f, indent=2)
    
    # Log artifacts to MLflow
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_artifact",
        local_path=artifact_path,
        artifact_path="outputs"
    )
    
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_artifact",
        local_path=metrics_path,
        artifact_path="metrics"
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
    # Return negative loss (to minimize) and accuracy (to maximize)
    return -test_metrics["test_loss"], test_metrics["test_accuracy"]


if __name__ == "__main__":
    main()
