"""Testing elements of the static state environement"""

from application.ann.environments.base_environments.static_state_environemnt import (
    StaticStateEnvironemnt,
)

test_config = {
    "env_map": "",
    "map_dimensions": "4",
    "start_location": "0",
    "max_number_of_genrations": "",
    "max_generation_duration": "",
    "fitness_threshold": "",
    "new_generation_threshold": "",
}


# def test_static_state_init() -> None:
#     """Test the generation and setting of the static state env"""
#         test_environemnt: StaticStateEnvironemnt = StaticStateEnvironemnt(env_config = test_config)
