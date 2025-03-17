"""Utilities or functions that are useful across all the different
modules in this package can be defined here."""

import os
import logging
import logging.config
import yaml
import mlflow
import time


logger = logging.getLogger(__name__)


def setup_logging(
    logging_config_path="./conf/logging.yaml", default_level=logging.INFO
):
    """Set up configuration for logging utilities.

    Parameters
    ----------
    logging_config_path : str, optional
        Path to YAML file containing configuration for Python logger,
        by default "./conf/logging.yaml"
    default_level : logging object, optional, by default logging.INFO
    """

    try:
        with open(logging_config_path, "rt", encoding="utf-8") as file:
            log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    except Exception as error:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=default_level,
        )
        logger.info(error)
        logger.info("Logging config file is not found. Basic config is being used.")


def mlflow_init(
    tracking_uri, exp_name, run_name, setup_mlflow=False, 
    autolog=False, resume=False
    ):
    """Initialise MLflow connection.

    Parameters
    ----------
    tracking_uri : string
        Tracking URI used for MLFlow
    exp_name : string
        Experiment name used for MLFlow
    run_name : string
        Run name for the experiment used for MLFlow
    setup_mlflow : bool, optional
        Choice to set up MLflow connection, by default False
    autolog : bool, optional
        Choice to set up MLflow's autolog, by default False
    resume : bool, optional
        Choice to resume using the latest previous run with the same 
        name, by default False

    Returns
    -------
    init_success : bool
        Boolean value indicative of success
        of intialising connection with MLflow server.

    mlflow_run : Union[None, `mlflow.entities.Run` object]
        On successful initialisation, the function returns an object
        containing the data and properties for the MLflow run.
        On failure, the function returns a null value.
    """
    init_success = False
    mlflow_run = None
    if setup_mlflow:
        try:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_experiment(exp_name)
            mlflow.enable_system_metrics_logging()

            if autolog:
                mlflow.autolog()

            if "MLFLOW_HPTUNING_TAG" in os.environ: run_name += "-hp"

            base_run_name = run_name
            
            if resume:
                # Try to find the most recent run with the same prefix name
                client = mlflow.tracking.MlflowClient()
                experiment = client.get_experiment_by_name(exp_name)
                if experiment:
                    runs = client.search_runs(
                        experiment_ids=[experiment.experiment_id],
                        filter_string=f"tags.mlflow.runName LIKE '{base_run_name}-%'",
                        order_by=["attribute.start_time DESC"],
                        max_results=1
                    )
                    if runs:
                        # Resume the most recent run
                        mlflow.start_run(run_id=runs[0].info.run_id)
                        logger.info(f"Resuming previous run: {runs[0].info.run_name}")
                    else:
                        # No previous run found, create a new one
                        run_name = f"{base_run_name}-{int(time.time())}"
                        mlflow.start_run(run_name=run_name)
                        logger.info(f"No previous run found. Starting new run: {run_name}")
                else:
                    # Experiment not found, create a new run
                    run_name = f"{base_run_name}-{int(time.time())}"
                    mlflow.start_run(run_name=run_name)
            else:
                # Start a new run with timestamp
                run_name = f"{base_run_name}-{int(time.time())}"
                mlflow.start_run(run_name=run_name)

            set_tag = lambda env_var, tag_name='': mlflow.set_tag(
                tag_name if tag_name != '' else env_var.lower(), 
                os.environ.get(env_var)
            ) if env_var in os.environ else None
            set_tag("MLFLOW_HP_TUNING_TAG", "hptuning_tag")
            set_tag("JOB_UUID")
            set_tag("JOB_NAME")

            mlflow_run = mlflow.active_run()
            init_success = True
            logger.info("MLflow initialisation has succeeded.")
            logger.info("UUID for MLflow run: %s", mlflow_run.info.run_id)
        except Exception as e:
            logger.error("MLflow initialisation has failed.")
            logger.error(e)

    return init_success, mlflow_run


def mlflow_log(mlflow_init_status, log_function, **kwargs):
    """Custom function for utilising MLflow's logging functions.

    This function is only relevant when the function `mlflow_init`
    returns a "True" value, translating to a successful initialisation
    of a connection with an MLflow server.

    Parameters
    ----------
    mlflow_init_status : bool
        Boolean value indicative of success of intialising connection
        with MLflow server.
    log_function : str
        Name of MLflow logging function to be used.
        See https://www.mlflow.org/docs/latest/python_api/mlflow.html
    **kwargs
        Keyword arguments passed to `log_function`.
    """
    if mlflow_init_status:
        try:
            method = getattr(mlflow, log_function)
            method(
                **{
                    key: value
                    for key, value in kwargs.items()
                    if key in method.__code__.co_varnames
                }
            )
        except Exception as error:
            logger.error(error)
