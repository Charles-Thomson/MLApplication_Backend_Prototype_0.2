"""generate the intances for trainning of the ann"""
import json
import numpy as np
from application.ann.environments.enviornment_types.environment_factory import (
    EnvironmentFactory,
)

# json_structure = {
#     "env_type": "",
#     "agent_type": ""
#     "env_data": {
#                     "env_map": "",
#                     "map_dimensions": "",
#                     "start_location": "",
#                     "max_number_of_genrations"
#                     "max_generation_duration": "",
#                     "fitness_threshold": "",
#                     "new_generation_threshold": ""
#                 },
#     "ann_data": {
#                 "weight_init_huristic": "",
#                 "hidden_activation_func": "",
#                 "output_activation_func": "",
#                 "new_generation_func": "",
#                 }
# }


class Instance:
    """
    The generated instance class
    """

    def __init__(self, id, environment, agent):
        self.id = id
        self.environment = environment
        self.agent = agent
        self.memeory = []  # this will be converted into a db model

    def run(self):
        """run the instance"""
        return ""


def new_instance(config: json) -> Instance:
    """Generate a new instance based on the given config settings
    var: config - the given config settings as json
    rtn: Callable object
    """

    insatnce_type: str = config["insatnce_type"]

    # Need to make the env json config file

    env_config: dict = format_env_config(config["env_data"])

    environment: object = EnvironmentFactory.make_env(
        env_type=config["env_type"], config=env_config
    )

    this_instance = Instance(id=id, environment=environment, agent=agent)

    return this_instance


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
    env_config["start_location"] = (start_x, start_y)

    env_config["max_number_of_genrations"] = int(config["max_number_of_genrations"])
    env_config["max_generation_duration"] = int(config["max_generation_duration"])
    env_config["fitness_threshold"] = float(config["fitness_threshold"])
    env_config["new_generation_threshold"] = int(config["new_generation_threshold"])

    return env_config
