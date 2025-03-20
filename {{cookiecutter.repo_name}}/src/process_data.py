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
        ),
        log_dir=args.get("log_dir", None)
    )

    raw_data_dir_path = args["raw_data_dir_path"]
    dataset = {{cookiecutter.src_package_name_short}}.data_prep.datasets.DummyDataset(
        raw_data_dir_path
    )

    processed_data_dir_path = args["processed_data_dir_path"]
    os.makedirs(args["processed_data_dir_path"], exist_ok=True)

    logger.info(
        "Copying files from %s to %s.",
        raw_data_dir_path,
        processed_data_dir_path
    )
    dataset.save_data(processed_data_dir_path)

    logger.info("All raw data has been processed.")


if __name__ == "__main__":
    main()