"""Dataset classes for defining how datasets are to be loaded."""

import glob
import os

import pandas as pd


class HdbDataset:
    """HDB Dataset class."""

    def __init__(self, data_dir_path: str) -> None:
        if not os.path.isdir(data_dir_path):
            e = "Path is not a directory, or does not exist: {}".format(data_dir_path)
            raise ValueError(e)
        self.data_dir_path = data_dir_path

    def load_data(self) -> pd.DataFrame:
        """
        Import .csv as DataFrame. Print error if unable to.

        Returns:
            df (pd.DataFrame): A concatenated DataFrame
        """
        try:
            csv_files = glob.glob(self.data_dir_path + "/*.csv")
            if not csv_files:
                raise ValueError(f"No CSV files found in {self.data_dir_path}")
            df_list = (pd.read_csv(file) for file in csv_files)
            self.df = pd.concat(df_list, ignore_index=True)
            return self.df
        except Exception as err:
            raise Exception(f"Failed to load data: {str(err)}") from err

    ## Create any other functions that you need in the Dataset class
