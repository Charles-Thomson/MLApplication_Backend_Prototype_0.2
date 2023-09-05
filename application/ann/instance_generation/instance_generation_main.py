"""generate the intances for trainning of the ann"""
import json
import numpy as np
from typing import Generator

from functools import partial

from application.ann.environments.environment_types.environment_factory import (
    EnvironmentFactory,
)

from application.ann.neural_networks.generational_functions.generational_functions_factory import (
    GenerationalFunctionsFactory,
)
from application.ann.neural_networks.hidden_layer_activation_functions.hidden_layer_functions_factory import (
    HiddenLayerActvaitionFactory,
)
from application.ann.neural_networks.output_layer_activation_functions.output_layer_functions_factory import (
    OutputLayerActvaitionFactory,
)
from application.ann.neural_networks.weight_huristics.weight_huristics_factory import (
    WeightHuristicsFactory,
)

from application.ann.agents.agent_generator import new_agent_generator


# json_structure = {
#     "env_type": "",
#     "agent_type": ""
#     "env_config": {
# "env_map": "",
# "map_dimensions": "",
# "start_location": "",
#      },
#        "instance_config": {
#         "max_number_of_genrations"
#         "max_generation_duration": "",
#         "fitness_threshold": "",
#         "new_generation_threshold": ""
#      }
#     "ann_config": {
#                 "weight_init_huristic": "",
#                 "hidden_activation_func": "",
#                 "output_activation_func": "",
#                 "new_generation_func": "",
#                 "hidden_layer_shape": "",
#                 "ouput_layer_shape": ""
#                 }
# }


class Instance:
    """
    The generated instance class
    """

    def __init__(self, id, environment, agent_generator, instance_config: dict):
        self.id: str = id
        self.environment: object = environment
        self.memeory = []  # this will be converted into a db model
        self.generation: int = 0

        self.fitness_threshold: float = instance_config["fitness_threshold"]
        self.max_number_of_generation: int = instance_config["max_number_of_genrations"]
        self.new_generation_threshold: int = instance_config["new_generation_threshold"]
        self.max_generation_duration: int = instance_config["max_generation_duration"]
        self.agent_generator: callable = agent_generator

    def run(self):
        """run the instance"""
        return ""


def new_instance(config: json) -> Instance:
    """Generate a new instance based on the given config settings
    var: config - the given config settings as json
    rtn: Callable object
    """

    env_config: dict = format_env_config(config["env_data"])

    ann_config_formatted: dict = format_ann_config(config["ann_data"])

    instance_config_formatted: dict = format_instance_config(config["insatnce_config"])

    environment: object = EnvironmentFactory.make_env(
        env_type=config["env_type"], config=env_config
    )

    agent_generater: callable = partial(
        new_agent_generator,
        ann_config=ann_config_formatted,
        agent_type=config["agent_type"],
    )

    this_instance = Instance(
        id=id,
        environment=environment,
        agent_generator=agent_generater,
        instance_config=instance_config_formatted,
    )

    return this_instance


def format_instance_config(config: dict) -> dict:
    """Format the json config to the appropriate types"""
    this_instance_config = {
        "max_number_of_genrations": "",
        "max_generation_duration": "",
        "fitness_threshold": "",
        "new_generation_threshold": "",
    }

    this_instance_config["max_number_of_genrations"] = int(
        config["max_number_of_genrations"]
    )
    this_instance_config["max_generation_duration"] = int(
        config["max_generation_duration"]
    )
    this_instance_config["fitness_threshold"] = float(config["fitness_threshold"])
    this_instance_config["new_generation_threshold"] = int(
        config["new_generation_threshold"]
    )

    return this_instance_config


def format_ann_config(ann_config: dict) -> dict:
    """Format the ann config from dict[str:str] to dict[str:type]"""
    this_ann_confg: dict = {
        "weight_init_huristic": "",
        "hidden_activation_func": "",
        "output_activation_func": "",
        "new_generation_func": "",
        "input_to_hidden_connections": "",
        "hidden_to_output_connections": "",
    }

    this_ann_confg["weight_init_huristic"] = WeightHuristicsFactory.get_huristic(
        ann_config["weight_init_huristic"]
    )
    this_ann_confg[
        "hidden_activation_func"
    ] = HiddenLayerActvaitionFactory.get_hidden_activation_func(
        ann_config["hidden_activation_func"]
    )
    this_ann_confg[
        "output_activation_func"
    ] = OutputLayerActvaitionFactory.get_output_activation_func(
        ann_config["output_activation_func"]
    )
    this_ann_confg[
        "new_generation_func"
    ] = GenerationalFunctionsFactory.get_generation_func(
        ann_config["new_generation_func"]
    )

    this_ann_confg["input_to_hidden_connections"]: tuple[int, int] = eval(
        ann_config["input_to_hidden_connections"]
    )
    this_ann_confg["hidden_to_output_connections"]: tuple[int, int] = eval(
        ann_config["hidden_to_output_connections"]
    )

    return this_ann_confg


def format_env_config(config: dict) -> dict:
    """Format the Json data to a dict to be passed to the environment factory
    var: config - Recived json file
    rtn: env_config - Json file in dict format
    """

    env_config = {
        "env_map": "",
        "map_dimensions": "",
        "start_location": "",
        "max_number_of_genrations": "",
        "max_generation_duration": "",
        "fitness_threshold": "",
        "new_generation_threshold": "",
    }

    env_map_string: str = config["env_map"]
    env_map_unshaped: np.array = np.fromstring(env_map_string, dtype=int, sep=",")
    reshape_val: int = int(config["map_dimensions"])

    env_map_shaped: np.array = env_map_unshaped.reshape(reshape_val, -1)
    env_config["env_map"] = env_map_shaped

    env_config["map_dimensions"] = int(config["map_dimensions"])

    start_x, start_y = config["start_location"].split(",")
    env_config["start_location"] = (int(start_x), int(start_y))

    env_config["max_number_of_genrations"] = int(config["max_number_of_genrations"])
    env_config["max_generation_duration"] = int(config["max_generation_duration"])
    env_config["fitness_threshold"] = float(config["fitness_threshold"])
    env_config["new_generation_threshold"] = int(config["new_generation_threshold"])

    return env_config
