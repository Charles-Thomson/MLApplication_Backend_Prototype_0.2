import pytest
import numpy as np
from application.ann.instance_generation.instance_generation_main import (
    new_instance,
)

from application.ann.agent_brains.brain_factory import BrainFactory
from application.ann.agent_brains.static_state_brain import BrainInstance


test_config = {
    "env_type": "Static_State",
    "agent_type": "Static_State",
    "env_config": {
        "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "map_dimensions": "4",
        "start_location": "1,1",
        "max_number_of_genrations": "2",
        "max_generation_size": "2",
        "fitness_threshold": "2",
        "new_generation_threshold": "2",
    },
    "instance_config": {
        "max_number_of_genrations": "2",
        "max_generation_size": "2",
        "fitness_threshold": "2",
        "new_generation_threshold": "2",
    },
    "ann_config": {
        "weight_init_huristic": "he_weight",
        "hidden_activation_func": "linear_activation_function",
        "output_activation_func": "argmax_activation",
        "new_generation_func": "crossover_weights_average",
        "input_to_hidden_connections": "(24,9)",
        "hidden_to_output_connections": "(9,9)",
    },
}


def test_instance_generation() -> None:
    test_instance: object = new_instance(test_config)

    assert isinstance(test_instance.instance_id, str)
    assert isinstance(test_instance.environment, object)
    assert isinstance(test_instance.generation_number, int)
    assert isinstance(test_instance.fitness_threshold, float)

    assert isinstance(test_instance.max_number_of_generations, int)
    assert isinstance(test_instance.new_generation_threshold, int)
    assert isinstance(test_instance.max_generation_size, int)
    assert callable(test_instance.agent_generator) is True
