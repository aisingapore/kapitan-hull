"""
This script is for training a model on the MNIST dataset.
"""
import os
import logging
import omegaconf
import hydra
import mlflow
import torch

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


# pylint: disable = no-value-for-parameter
@hydra.main(version_base=None, config_path="../conf/base", config_name="pipelines.yaml")
def main(args):
    """This is the main function for training the model.

    Parameters
    ----------
    args : omegaconf.DictConfig
        An omegaconf.DictConfig object containing arguments for the main function.
    """
    args = args["train_model"]

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(
        logging_config_path=os.path.join(
            hydra.utils.get_original_cwd(), "conf/base/logging.yaml"
        )
    )

    mlflow_init_status, mlflow_run = {{cookiecutter.src_package_name_short}}.general_utils.mlflow_init(
        args, setup_mlflow=args["setup_mlflow"], autolog=args["mlflow_autolog"]
    )
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_params",
        params={
            "learning_rate": args["lr"],
            "gamma": args["gamma"],
            "seed": args["seed"],
            "epochs": args["epochs"],
        },
    )

    torch.manual_seed(args["seed"])

    use_cuda = not args["no_cuda"] and torch.cuda.is_available()
    if use_cuda:
        device = torch.device("cuda")
    elif not args["no_mps"] and torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    train_kwargs = {"batch_size": args["train_bs"]}
    test_kwargs = {"batch_size": args["test_bs"]}
    if use_cuda:
        cuda_kwargs = {"num_workers": 1, "pin_memory": True, "shuffle": True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    train_dataset = {{cookiecutter.src_package_name_short}}.data_prep.datasets.MNISTDataset(
        args["data_dir_path"], "train.csv", to_grayscale=True, to_tensor=True
    )
    test_dataset = {{cookiecutter.src_package_name_short}}.data_prep.datasets.MNISTDataset(
        args["data_dir_path"], "test.csv", to_grayscale=True, to_tensor=True
    )
    train_loader = torch.utils.data.DataLoader(train_dataset, **train_kwargs)
    test_loader = torch.utils.data.DataLoader(test_dataset, **test_kwargs)

    model = {{cookiecutter.src_package_name_short}}.modeling.models.Net().to(device)
    optimiser = torch.optim.Adadelta(model.parameters(), lr=args["lr"])
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimiser, step_size=1, gamma=args["gamma"]
    )

    for epoch in range(1, args["epochs"] + 1):
        curr_train_loss = {{cookiecutter.src_package_name_short}}.modeling.utils.train(
            args, model, device, train_loader, optimiser, epoch, mlflow_init_status
        )
        curr_test_loss, curr_test_accuracy = {{cookiecutter.src_package_name_short}}.modeling.utils.test(
            model, device, test_loader, epoch, mlflow_init_status
        )

        if epoch % args["model_checkpoint_interval"] == 0:
            logger.info("Exporting the model for epoch %s.", epoch)

            model_checkpoint_path = os.path.join(
                args["model_checkpoint_dir_path"], "model.pt"
            )
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "epoch": epoch,
                    "optimiser_state_dict": optimiser.state_dict(),
                    "train_loss": curr_train_loss,
                    "test_loss": curr_test_loss,
                },
                model_checkpoint_path,
            )
            {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
                mlflow_init_status,
                "log_artifact",
                local_path=model_checkpoint_path,
                artifact_path="model",
            )

        scheduler.step()

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_dict",
        dictionary=omegaconf.OmegaConf.to_container(args, resolve=True),
        artifact_file="train_model_config.json",
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

    return curr_test_loss, curr_test_accuracy


if __name__ == "__main__":
    main()
