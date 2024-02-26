"""Dataset classes for defining how datasets are to be loaded.
"""

import os
import shutil

class DummyDataset():
    """Dummy dataset class."""
    
    def __init__(self, data_dir_path) -> None:
        if not os.path.isdir(data_dir_path):
            e = "Path is not a directory, or does not exist: {}".format(data_dir_path)
            logger.error(e)
            raise ValueError(e)
        self.data_dir_path = data_dir_path

    def save_data(self, processed_data_dir_path) -> None:
        shutil.copytree(
            self.data_dir_path,
            processed_data_dir_path,
            dirs_exist_ok=True
        )