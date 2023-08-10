"""generate the intances for trainning of the ann"""
import json
from application.ann.agents.agent_selection import new_agent
from application.ann.environments.environment_selection import new_environment
from application.ann.agent_brains.brain_selection import new_brain

# json_structure = {
#     "insatnce_type": "",
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
    def __init__(self, environment, agent):
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

    environent = environments_available[insatnce_type]
    agent_brain = brains_available[insatnce_type]
    agent = agents_available[insatnce_type]

    environments_available = {
        "static_state_based": "state_based(env_config=env_config)",
        "dynamic_coordiate_based": "coordinate_based(env_config=env_config)"
    }

    brains_available = {
        "static_state_based": "state_based(ann_config=ann_config)",
        "dynamic_coordiate_based": "coordinate_based(ann_config=ann_config)"
    }

    agents_available = {
        "static_state_based": "state_based(brain=brain)",
        "dynamic_coordiate_based": "coordinate_based(brain=brain)"
    }

    

    this_instance = Instance(environment=environent, agent=agent)

    return this_instance
