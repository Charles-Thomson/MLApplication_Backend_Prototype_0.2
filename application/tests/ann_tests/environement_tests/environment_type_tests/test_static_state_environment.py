"""Testing elements of the static state environement"""
import pytest

from application.ann.environments.environment_types.environment_factory import (
    EnvironmentFactory,
)

from application.ann.instance_generation.instance_generation_main import (
    format_env_config,
)

test_env_type: str = "Static_State"

test_config = {
    "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
    "map_dimensions": "4",
    "start_location": "1",
    "max_number_of_genrations": "2",
    "max_generation_duration": "2",
    "fitness_threshold": "2",
    "new_generation_threshold": "2",
}


env_config: dict = format_env_config(test_config)
pytest.static_state_test_env = EnvironmentFactory.make_env(
    test_env_type, config=env_config
)


def test_get_env_type() -> None:
    """Test the reurned env type"""

    assert pytest.static_state_test_env.get_env_type() == test_env_type


def test_environment_observation() -> None:
    """Test the collection of observation data from the environement"""

    observation_data = pytest.static_state_test_env.environment_observation()

    assert len(observation_data) == 24
    assert (x == type(float) for x in observation_data)


bounds = env_config["map_dimensions"] - 1
total_states: int = env_config["map_dimensions"] * env_config["map_dimensions"] - 1


@pytest.mark.parametrize(
    "action,new_location,termination_state",
    [
        (0, (0, 0), False),
        (1, (1, 0), False),
        (2, (2, 0), False),
        (3, (0, 1), False),
        (4, (1, 1), False),
        (5, (1, 2), False),
        (6, (2, 0), False),
        (7, (2, 1), False),
        (8, (2, 2), False),
    ],
)
def test_environement_step(action, new_location, termination_state) -> None:
    """Test a single step in the enviornment"""
    pytest.static_state_test_env.current_coords = (1, 1)
    new_coords, termination, reward = pytest.static_state_test_env.step(action)

    assert new_coords == new_location
    assert termination == termination_state


# Param termination testing data
@pytest.mark.parametrize(
    "location,action,new_location,termination",
    [
        ((0, 0), 0, 0, True),
        ((0, 0), 1, 0, True),
        ((0, 0), 2, 0, True),
        ((0, 0), 3, 0, True),
        ((0, 0), 6, 0, True),
        ((0, bounds), 0, bounds, True),
        ((0, bounds), 1, bounds, True),
        ((0, bounds), 2, bounds, True),
        ((0, bounds), 5, bounds, True),
        ((0, bounds), 8, bounds, True),
        ((bounds, 0), 0, total_states - bounds, True),
        ((bounds, 0), 3, total_states - bounds, True),
        ((bounds, 0), 6, total_states - bounds, True),
        ((bounds, 0), 7, total_states - bounds, True),
        ((bounds, 0), 8, total_states - bounds, True),
        ((bounds, bounds), 2, total_states, True),
        ((bounds, bounds), 5, total_states, True),
        ((bounds, bounds), 6, total_states, True),
        ((bounds, bounds), 7, total_states, True),
        ((bounds, bounds), 8, total_states, True),
    ],
)
def test_boundry_termination(location, action, new_location, termination):
    """holder"""
    pytest.static_state_test_env.current_coords = location
    new_state, this_termination, reward, info = pytest.static_state_test_env.step(
        action
    )
    assert new_state == new_location
    assert this_termination == termination
