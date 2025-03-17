"""Module for containing architectures/definition of models."""
import time


class DummyModel():
    """Dummy model that returns the input."""

    def __init__(self):
        pass

    def train(self, X=None, y=None):
        """'Trains' the dummy model.

        Parameters
        ----------
        X : Any
            Dummy feature data.
        y : Any
            Dummy target data.

        Returns
        -------
        None
        """
        time.sleep(1)

    def predict(self, x=''):
        """'Prediction' of the dummy model.

        Parameters
        ----------
        x : str
            Input string.
        
        Returns
        -------
        str
            Output string.
        """

        return x