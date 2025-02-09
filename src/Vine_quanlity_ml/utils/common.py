import os
import yaml
import logging
from box.exceptions import BoxValueError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns ConfigBox with dictionary-like behavior.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If the YAML file is empty or content is invalid.
        BoxValueError: If the YAML content cannot be parsed into a dictionary.

    Returns:
        ConfigBox: A ConfigBox object initialized from the YAML content.
    """
    try:
        # Check if the file exists
        if not os.path.exists(path_to_yaml):
            logger.error(f"The file at {path_to_yaml} does not exist.")
            raise FileNotFoundError(f"The file at '{path_to_yaml}' was not found.")

        # Read the YAML file
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)

        # Validate that the content is not None or empty
        if not content or not isinstance(content, dict):
            logger.error(f"The YAML file at {path_to_yaml} is invalid or not a dictionary.")
            raise ValueError(f"The YAML file at '{path_to_yaml}' must contain a valid dictionary.")

        logger.info(f"YAML file: {path_to_yaml} loaded successfully")
        return ConfigBox(content)

    except BoxValueError as bve:
        logger.error(f"Error parsing YAML file - expected a dictionary but got an invalid structure: {bve}")
        raise ValueError(
            f"Could not parse the YAML content in '{path_to_yaml}'. Make sure it is valid YAML and has key-value pairs.") from bve
    except Exception as e:
        logger.error(f"An error occurred while reading the YAML file: {e}")
        raise e




@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:x
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"




