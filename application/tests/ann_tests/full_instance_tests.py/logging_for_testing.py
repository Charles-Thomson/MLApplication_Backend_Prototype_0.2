"""Basic logging imports"""
import logging.handlers
import os

from functools import wraps
from typing import Any, Callable
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

new_logger = logging.getLogger()
filename = "application/tests/ann_tests/full_instance_tests.py/test_logs/log_file.log"

should_roll_over = os.path.isfile(filename)

handler = logging.handlers.RotatingFileHandler(filename=filename, backupCount=3)
if should_roll_over:
    handler.doRollover()
formatter = logging.Formatter(DEFAULT_FORMAT)
handler.setFormatter(formatter)
new_logger.addHandler(handler)
new_logger.propagate = False


# def generate_test_logger(
#     name: __name__, log_file: str, formatting: str = DEFAULT_FORMAT
# ):
#     """Generat a custom logger"""

#     new_logger = logging.getLogger(name)
#     filename = (
#         "application/tests/ann_tests/full_instance_tests.py/test_logs/log_file"
#     )

#     should_roll_over = os.path.isfile(filename)

#     handler = logging.handlers.RotatingFileHandler(
#         filename=filename, mode="w", backupCount=3
#     )
#     if should_roll_over:
#         handler.doRollover()
#     formatter = logging.Formatter(formatting)
#     handler.setFormatter(formatter)
#     new_logger.addHandler(handler)
#     new_logger.propagate = False

#     return new_logger


# test_logger = generate_test_logger(__name__ + "test_logger", "test_log.log")


def logger_test_brains_logging(func: Callable[..., Any]) -> Any:
    """Testing the logging for test brains"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        brains = func(*args)
        for brain in brains:
            new_logger.info(
                f"Brain: {brain.brain_id} - Generation: {brain.current_generation_number} Path: {brain.traversed_path} Fitness: {brain.fitness}"
            )

    return wrapper


with_test_brian_logging = logger_test_brains_logging
