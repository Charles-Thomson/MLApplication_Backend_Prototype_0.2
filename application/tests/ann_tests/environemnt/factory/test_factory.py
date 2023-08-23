"""Testing the generation of the environments via the environemnt_factory"""

from application.ann.environments.base_environments.environment_factory import (
    EnvironmentFactory,
)
from application.ann.environments.base_environments.static_state_environemnt import (
    StaticStateEnvironemnt,
)

env_config = {
    "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
    "map_dimensions": "4",
    "start_location": "1",
    "max_number_of_genrations": "2",
    "max_generation_duration": "2",
    "fitness_threshold": "2",
    "new_generation_threshold": "2",
}


# def test_environemnt_factory() -> None:
#     """Test the generation of ebvironmets from the factory"""
#     static_state: StaticStateEnvironemnt = EnvironmentFactory.make_env(
#         "Static_State", config=env_config
#     )

#     assert static_state == StaticStateEnvironemnt
