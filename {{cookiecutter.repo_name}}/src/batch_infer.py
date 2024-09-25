"""Script to conduct batch inferencing.
"""
import os
import datetime
import logging
import glob
import hydra
import jsonlines


import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


# pylint: disable = no-value-for-parameter
@hydra.main(version_base=None, config_path="../conf", config_name="batch_infer.yaml")
def main(args):
    """This main function does the following:
    - load logging config
    - gets list of files to be loaded for inferencing
    - loads trained model
    - conducts inferencing on data
    - outputs prediction results to a jsonline file
    - returns an error if there are no files/data specified to be inferred
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.join(
        hydra.utils.get_original_cwd(), "conf", "logging.yaml"
    )
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(logger_config_path)

    logger.info("Loading the model...")
    loaded_model = {{cookiecutter.src_package_name_short}}.modeling.utils.load_model()

    glob_expr = os.path.join(
        args["input_data_dir"], args["file_check_glob"]
    )
    logger.info("Conducting inferencing on text files...")

    jsonl_path = os.path.join(
        os.getcwd(), args["output_path"]
    )
    has_text = False # Checking if for loop is running

    for text_file in glob.glob(glob_expr):
        has_text = True
        text = open(text_file).read()
        pred_str = loaded_model.predict(text)

        curr_time = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        curr_res_jsonl = {
            "time": curr_time,
            "text_filepath": text_file,
            "prediction": pred_str,
        }

        with jsonlines.open(jsonl_path, mode="a") as writer:
            writer.write(curr_res_jsonl)
            writer.close()

    if not has_text:
        e = "Folder {} has no files to infer according to the given glob '{}'.".format(
            os.path.abspath(args["input_data_dir"]), args["file_check_glob"]
        )
        logger.error(e)
        raise FileNotFoundError(e)

    logger.info("Batch inferencing has completed.")
    logger.info("Output result location: %s", jsonl_path)


if __name__ == "__main__":
    main()