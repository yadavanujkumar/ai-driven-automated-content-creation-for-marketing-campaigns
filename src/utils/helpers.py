import logging
import re
import json
from typing import Any, Dict, List, Union


# Configure logging for the application
def configure_logging(log_file: str = "app.log", level: int = logging.INFO) -> None:
    """
    Configures the logging for the application.

    Args:
        log_file (str): The file where logs will be saved.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger().addHandler(logging.StreamHandler())


# Input sanitization
def sanitize_input(input_data: Union[str, Dict, List]) -> Union[str, Dict, List]:
    """
    Sanitizes input data to prevent injection attacks and ensure clean data.

    Args:
        input_data (Union[str, Dict, List]): The input data to sanitize.

    Returns:
        Union[str, Dict, List]: Sanitized input data.
    """
    if isinstance(input_data, str):
        # Remove potentially harmful characters
        sanitized = re.sub(r"[<>\"';]", "", input_data)
        return sanitized.strip()
    elif isinstance(input_data, dict):
        # Recursively sanitize dictionary values
        return {key: sanitize_input(value) for key, value in input_data.items()}
    elif isinstance(input_data, list):
        # Recursively sanitize list elements
        return [sanitize_input(item) for item in input_data]
    else:
        return input_data


# Error handling decorator
def handle_errors(default_return: Any = None):
    """
    A decorator to handle errors in functions and log them.

    Args:
        default_return (Any): The default value to return in case of an error.

    Returns:
        Callable: The wrapped function with error handling.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                return default_return
        return wrapper
    return decorator


# JSON utilities
def load_json(file_path: str) -> Dict:
    """
    Loads a JSON file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict: The content of the JSON file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to load JSON file {file_path}: {str(e)}", exc_info=True)
        return {}


def save_json(file_path: str, data: Dict) -> None:
    """
    Saves a dictionary as a JSON file.

    Args:
        file_path (str): The path to save the JSON file.
        data (Dict): The data to save.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Failed to save JSON file {file_path}: {str(e)}", exc_info=True)


# Example utility: Generate slug from a string
def generate_slug(text: str) -> str:
    """
    Generates a URL-friendly slug from a given string.

    Args:
        text (str): The input string.

    Returns:
        str: The generated slug.
    """
    sanitized_text = sanitize_input(text)
    slug = re.sub(r"[^\w\s-]", "", sanitized_text)  # Remove non-alphanumeric characters
    slug = re.sub(r"\s+", "-", slug)  # Replace spaces with hyphens
    return slug.lower()


# Example utility: Validate email address
def is_valid_email(email: str) -> bool:
    """
    Validates if the given string is a properly formatted email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_regex, email))


# Example utility: Chunk a list into smaller parts
def chunk_list(data: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Splits a list into smaller chunks of a specified size.

    Args:
        data (List[Any]): The list to split.
        chunk_size (int): The size of each chunk.

    Returns:
        List[List[Any]]: A list of chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


# Example utility: Flatten a nested list
def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flattens a nested list into a single list.

    Args:
        nested_list (List[List[Any]]): The nested list to flatten.

    Returns:
        List[Any]: The flattened list.
    """
    return [item for sublist in nested_list for item in sublist]