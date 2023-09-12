"""The decorator for logging"""
from functools import wraps
from typing import Any, Callable
import functools
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"


def generate_logger(name: __name__, log_file: str, formatting: str = DEFAULT_FORMAT):
    """Generat a custom logger"""

    new_logger = logging.getLogger(name)
    filename = "application/ann/logging_files/" + log_file
    handler = logging.FileHandler(filename=filename, mode="w")
    formatter = logging.Formatter(formatting)
    handler.setFormatter(formatter)
    new_logger.addHandler(handler)
    new_logger.propagate = False

    return new_logger


brains_log = generate_logger(__name__ + "brain_logger", "brain_logger.log")


def brain_logger(func: Callable[..., Any], brain_log: logging.Logger):
    """Basic logger deco for logging brain data"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        brains = func(*args)
        print(brains)
        for brain in brains:
            print(brain.brain_id)
            brain_log.info(
                f"Brain: {brain.brain_id} - Generation: {brain.current_generation_number} Path: {brain.traversed_path} Fitness: {brain.fitness}"
            )
        return brains

    return wrapper


with_brain_logging = functools.partial(brain_logger, brain_log=brains_log)
