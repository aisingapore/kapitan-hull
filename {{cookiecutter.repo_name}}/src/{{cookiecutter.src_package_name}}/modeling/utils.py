"""Utilities for model training and experimentation workflows.
"""
import time
import random
import logging

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}

logger = logging.getLogger(__name__)

def load_model():
    """Load dummy model.

    A sample utility function to be used.

    Returns
    -------
    loaded_model : 
        Object containing dummy model.
    """
    loaded_model = {{cookiecutter.src_package_name_short}}.modeling.models.DummyModel()

    return loaded_model


def train(model, epochs=5, learning_rate=0.01, batch_size=32):
    """Simulate training a model.

    Parameters
    ----------
    model : object
        The model to train.
    epochs : int, optional
        Number of epochs to train for, by default 5.
    learning_rate : float, optional
        Learning rate for training, by default 0.01.
    batch_size : int, optional
        Batch size for training, by default 32.

    Returns
    -------
    dict
        Dictionary containing training metrics.
    """
    logger.info(f"Starting training with {epochs} epochs, lr={learning_rate}, batch_size={batch_size}")
    
    metrics = {
        "train_loss": [],
        "train_accuracy": []
    }
    
    for epoch in range(1, epochs + 1):
        # Simulate training for 1 second
        time.sleep(1)
        
        # Generate fake metrics that improve over time
        loss = 1.0 - (0.15 * epoch) + random.uniform(-0.05, 0.05)
        loss = max(0.1, loss)  # Ensure loss doesn't go below 0.1
        accuracy = 0.5 + (0.08 * epoch) + random.uniform(-0.02, 0.02)
        accuracy = min(0.98, accuracy)  # Cap accuracy at 0.98
        
        metrics["train_loss"].append(loss)
        metrics["train_accuracy"].append(accuracy)
        
        logger.info(f"Epoch {epoch}/{epochs} - loss: {loss:.4f}, accuracy: {accuracy:.4f}")
    
    return metrics


def test(model, test_size=100):
    """Simulate testing a model.

    Parameters
    ----------
    model : object
        The model to test.
    test_size : int, optional
        Number of test samples, by default 100.

    Returns
    -------
    dict
        Dictionary containing test metrics.
    """
    logger.info(f"Evaluating model on {test_size} test samples")
    
    # Simulate a short evaluation time
    time.sleep(1)
    
    # Generate fake test metrics
    test_loss = random.uniform(0.1, 0.3)
    test_accuracy = random.uniform(0.85, 0.95)
    
    metrics = {
        "test_loss": test_loss,
        "test_accuracy": test_accuracy
    }
    
    logger.info(f"Test results - loss: {test_loss:.4f}, accuracy: {test_accuracy:.4f}")
    
    return metrics
