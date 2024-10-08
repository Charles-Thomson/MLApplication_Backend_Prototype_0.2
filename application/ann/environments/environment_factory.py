"""The factory for the environments"""
import json
from functools import partial
import numpy as np

from application.ann.environments.environment_protocol import EnvironemntProtocol

from application.ann.environments.observation_data.static_state_observation import (
    static_state_observation,
)


class EnvironmentFactory:
    """Factory class fot environments"""

    envs = {}

    @classmethod
    def make_env(cls, env_type: str, config: dict):
        """Make the env based on given type"""
        try:
            retreval = cls.envs[env_type]
        except KeyError as err:
            raise NotImplementedError(f"{env_type} is not implemented") from err

        return retreval(env_config=config)

    @classmethod
    def register(cls, type_name):
        """Register an env to the factory"""

        def deco(deco_cls):
            cls.envs[type_name] = deco_cls
            return deco_cls

        return deco


@EnvironmentFactory.register("Static_State")
class StaticStateEnvironemnt(EnvironemntProtocol):
    """Environment that operates on set movements between static states"""

    def __init__(self, env_config: json):
        self.environment_map: np.array = env_config["env_map"]

        dimension: int = env_config["map_dimensions"]

        self.max_step_count: int = 20

        self.start_coords: tuple[int, int] = env_config["start_location"]

        self.observation_function: callable = partial(
            static_state_observation, ncol=dimension
        )

        self.current_coords: tuple[int, int] = self.start_coords

        self.current_step: int = 0
        self.path: list[tuple[int, int]] = []

    def get_env_type(self) -> str:
        """Return the type of the environement
        rtn -> String: The type of the environement
        """
        return "Static_State"

    def get_environment_observation(self) -> np.array:
        """Get observation data from the environment"""

        return self.observation_function(self.current_coords, self.environment_map)

    def setup_call(self):
        """A call for an agent to request the set up data from the env
        - Currently only used to pass start location
        """

        return self.current_coords

    def step(self, action: int) -> tuple[int, float, bool]:
        """Process the next step/movment in the environment
        var - action: the given action from the agent
        rtn: new_coords, termination, reward
        """

        reward: float = self.calculate_reward(self.current_coords)
        new_state_x, new_state_y = self.process_action(action)
        termination: bool = self.termination_check(new_state_x, new_state_y)
        self.path.append(self.current_coords)

        new_coords = (new_state_x, new_state_y)

        self.current_coords = new_coords
        self.current_step += 1

        return new_coords, termination, reward

    def remove_goal(self, current_state_x: int, current_state_y: int):
        """Remove goal location from maze once reached - sets to open i.e '1'"""
        self.environment_map[current_state_x, current_state_y] = 1

    def calculate_reward(self, current_coords: tuple[int]) -> float:
        """Calculate the reward for the previous step"""

        current_state_x, current_state_y = current_coords

        value_at_new_state = get_location_value(
            self.environment_map, (current_state_x, current_state_y)
        )

        if (current_state_x, current_state_y) in self.path:
            return 0.0

        match value_at_new_state:
            case 1:  # Open Tile
                return 0.15

            case 2:  # Obstical
                return 0.0

            case 3:  # goal
                self.remove_goal(current_state_x, current_state_y)
                return 3.0

    def termination_check(self, new_state_x: int, new_state_y: int) -> bool:
        """Check if the agent action has lead to termination of the agent"""

        termination_conditions: list = [
            new_state_x < 0,
            new_state_y < 0,
            self.current_step >= self.max_step_count,
            get_location_value(self.environment_map, (new_state_x, new_state_y)) == 2,
        ]

        if any(termination_conditions):
            return True

        return False

    def process_action(self, action: int) -> tuple[int]:
        """Process the given action"""

        hrow, hcol = self.current_coords

        match action:
            case 0:  # Up + Left
                hrow -= 1
                hcol -= 1

            case 1:  # Up
                hrow -= 1

            case 2:  # Up + Right
                hrow -= 1
                hcol += 1

            case 3:  # left
                hcol -= 1

            case 4:  # No Move
                pass

            case 5:  # Right
                hcol += 1

            case 6:  # Down + Left
                hrow += 1
                hcol -= 1

            case 7:  # Down
                hrow += 1

            case 8:  # Down + Right
                hcol += 1
                hrow += 1

        return (hrow, hcol)


def to_coords(ncol: int, state: int):
    """Convert state value to map coords"""
    return divmod(state, ncol)


def to_state(ncol: int, coords: tuple[int, int]):
    """Convert map coords to state value"""
    return (coords[0] * ncol) + coords[1]


def get_location_value(env_map: np.array, coords: tuple):
    """Get the value of a location in the env"""
    try:
        value = env_map[coords[0]][coords[1]]
        return value
    except IndexError:
        return 2  # Termination condition
