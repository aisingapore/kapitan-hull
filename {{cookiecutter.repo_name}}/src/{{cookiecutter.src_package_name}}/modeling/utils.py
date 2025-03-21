"""Utilities for model training and experimentation workflows.
"""
import time
import random
import logging

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}

logger = logging.getLogger(__name__)


def train(mlflow_init_status, model, dataset, epoch, learning_rate=0.01, batch_size=32):
    """Simulate training a model.

    Parameters
    ----------
    mlflow_init_status : bool
        Boolean value indicative of success of intialising connection
        with MLflow server.
    model : object
        The model to train.
    dataset : object
        The dataset.
    epoch : int
        Current epoch value.
    learning_rate : float, optional
        Learning rate for training, by default 0.01.
    batch_size : int, optional
        Batch size for training, by default 32.

    Returns
    -------
    loss : float
        Simulated loss value for the training dataset.
    """
    
    model.train()
    
    # Generate fake metrics that improve over time
    loss = 1.0 - (0.15 * epoch) + random.uniform(-0.05, 0.05)
    loss = max(0.1, loss)  # Ensure loss doesn't go below 0.1
    accuracy = 0.5 + (0.08 * epoch) + random.uniform(-0.02, 0.02)
    accuracy = min(0.98, accuracy)  # Cap accuracy at 0.98
    
    logger.info(f"Epoch {epoch} - loss: {loss:.4f}, accuracy: {accuracy:.4f}")
    
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_metric",
        key="train_loss",
        value=loss,
        step=epoch,
    )

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_metric",
        key="train_accuracy",
        value=accuracy,
        step=epoch,
    )

    return loss


def test(mlflow_init_status, model, dataset, epoch, test_size=100):
    """Simulate testing a model.

    Parameters
    ----------
    mlflow_init_status : bool
        Boolean value indicative of success of intialising connection
        with MLflow server.
    model : object
        The model to test.
    dataset : object
        The dataset.
    epoch : int
        Current epoch value.
    test_size : int, optional
        Number of test samples, by default 100.

    Returns
    -------
    test_loss : float
        Average loss value for the test dataset.
    test_accuracy : float
        Accuracy value for the test dataset.
    """
    logger.info(f"Evaluating model on {test_size} test samples")
    
    model.predict()
    
    # Generate fake test metrics
    test_loss = random.uniform(0.1, 0.3)
    test_accuracy = random.uniform(0.85, 0.95)
    
    logger.info(f"Test results - loss: {test_loss:.4f}, accuracy: {test_accuracy:.4f}")
    
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_metric",
        key="test_loss",
        value=test_loss,
        step=epoch
    )

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_metric",
        key="test_accuracy",
        value=test_accuracy,
        step=epoch
    )

    return test_loss, test_accuracy


def load_model():
    """Load dummy model.

    A sample utility function to be used.

    Returns
    -------
    loaded_model : object
        Object containing dummy model.
    """
    loaded_model = {{cookiecutter.src_package_name_short}}.modeling.models.DummyModel()

    return loaded_model

