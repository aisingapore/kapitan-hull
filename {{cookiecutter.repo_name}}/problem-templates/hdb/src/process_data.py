"""
This script is a template for processing data.
"""

import os
import shutil
import logging
import hydra

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


# pylint: disable = no-value-for-parameter
@hydra.main(version_base=None, config_path="../conf", config_name="process_data.yaml")
def main(args) -> None:
    """This function is a template to process data.

    Parameters
    ----------
    args: omegaconf.DictConfig
        An omegaconf.DictConfig object containing arguments for the main function.
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(
        logging_config_path=os.path.join(
            hydra.utils.get_original_cwd(), "conf", "logging.yaml"
        )
    )

    raw_data_dir_path = args["raw_data_dir_path"]
    dataset = {{cookiecutter.src_package_name_short}}.data_prep.datasets.HdbDataset(
        raw_data_dir_path
    )
    
    raw_data = dataset.load_data()

    processed_data_dir_path = args["processed_data_dir_path"]
    os.makedirs(args["processed_data_dir_path"], exist_ok=True)

    ## Example code, adjust or use your own code
    logger.info("Processing raw data")
    X_train, X_test, y_train, y_test = {{cookiecutter.src_package_name_short}}.data_prep.transforms.transform(
       raw_data, args["test_size"], args["seed"]
    )
    X_train.to_csv(os.path.join(processed_data_dir_path, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(processed_data_dir_path, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(processed_data_dir_path, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(processed_data_dir_path, "y_test.csv"), index=False)
    logger.info("All raw data has been processed and saved.")
    ## Example code, adjust or use your own code

if __name__ == "__main__":
    main()