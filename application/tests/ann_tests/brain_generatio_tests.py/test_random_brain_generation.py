"""Testing the gernation of a randomly weighted brain"""
import pytest
from application.ann.instance_generation.instance_generation_main import (
    format_ann_config,
)

test_ann_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "(24,9)",
    "hidden_to_output_connections": "(9,9)",
}


def test_formatting_ann_config() -> None:
    """Testing the formatting of the ann config file"""

    foramtted_test_config = format_ann_config(ann_config=test_ann_config)

    assert foramtted_test_config is dict
    # assert callable(foramtted_test_config["weight_init_huristic"]) is True
    assert callable(foramtted_test_config["hidden_activation_func"]) is True
    assert callable(foramtted_test_config["output_activation_func"]) is True
    assert callable(foramtted_test_config["new_generation_func"]) is True
    assert foramtted_test_config["input_to_hidden_connections"] == (24, 9)
    assert foramtted_test_config["hidden_to_output_connections"] == (9, 9)
