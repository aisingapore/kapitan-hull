"""Module for containing architectures/definition of models."""


class DummyModel():
    """Dummy model that returns the input."""

    def __init__(self):
        pass

    def predict(self, x):
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