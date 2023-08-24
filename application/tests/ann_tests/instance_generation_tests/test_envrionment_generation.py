"""Test the generaition of an environement in the instance generation file"""


from application.ann.environments.base_environments.environment_factory import (
    EnvironmentFactory,
)
from application.ann.environments.base_environments.static_state_environemnt import (
    StaticStateEnvironemnt,
)

from application.ann.instance_generation.instance_generation_main import (
    format_env_config,
)


test_config = {
    "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
    "map_dimensions": "4",
    "start_location": "1",
    "max_number_of_genrations": "2",
    "max_generation_duration": "2",
    "fitness_threshold": "2",
    "new_generation_threshold": "2",
}

test_env_type: str = "Static_State"


def test_environment_generation() -> None:
    """Test the generation of an environement"""

    env_config: dict = format_env_config(test_config)
    static_state_test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
        test_env_type, config=env_config
    )

    assert static_state_test_env.get_env_type() == "Static_State"
