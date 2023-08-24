"""Testing elements of the static state environement"""
import pytest

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


# Shared env across testing in tis instance
env_config: dict = format_env_config(test_config)
pytest.static_state_test_env = EnvironmentFactory.make_env(
    test_env_type, config=env_config
)


class TestStaticStateEnvironemntCore:
    """Test class for the Static State environement"""

    def test_get_env_type(self) -> None:
        """Test the reurned env type"""

        assert pytest.static_state_test_env.get_env_type() == test_env_type

    def test_environment_observation(self) -> None:
        """Test the collection of observation data from the environement"""

        observation_data = pytest.static_state_test_env.environment_observation()

        assert len(observation_data) == 24
        assert (x == type(float) for x in observation_data)


def test_env_boundry_termiantion() -> None:
    """Test for termination on each of the boundries""" ""


def test_env_obstical_termination() -> None:
    """Test for termination when agent hits obstical in env"""

    test_config = {
        "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "map_dimensions": "4",
        "start_location": "0",
        "max_number_of_genrations": "2",
        "max_generation_duration": "2",
        "fitness_threshold": "2",
        "new_generation_threshold": "2",
    }

    test_env_type: str = "Static_State"

    env_config: dict = format_env_config(test_config)
    static_state_test_env = EnvironmentFactory.make_env(
        test_env_type, config=env_config
    )

    TOP_LEFT_STATE = 0
    TOP_RIGHT_STATE = env_config["map_dimensions"] - 1
    BOTTOM_LEFT_STATE = (len(env_config["env_map"]) - env_config["map_dimensions"]) + 1
    BOTTOM_RIGHT_STATE = len(env_config["env_map"])

    # Top left Corner Boundries
    static_state_test_env.current_state = TOP_LEFT_STATE


@pytest.mark.parametrize(
    "location,action,new_location,termination",
    [
        (0, 0, 0, True),
        (0, 1, 0, True),
        (0, 2, 0, True),
        (0, 3, 0, True),
        (0, 6, 0, True),
    ],
)
def test_steping(location, action, new_location, termination):
    """holder"""
    pytest.static_state_test_env.current_coords = (0, 0)
    new_state, this_termination, reward, info = pytest.static_state_test_env.step(
        action
    )
    assert new_state == new_location
    assert this_termination == termination
