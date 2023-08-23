"""Defining the static state environent"""
import json
from functools import partial
import numpy as np

from application.ann.environments.base_environments.environment_protocol import (
    EnvironemntProtocol,
)

from application.ann.environments.base_environments.environment_factory import (
    EnvironmentFactory,
)

from application.ann.environments.observation_data import static_state_observation

# Not sure if still needed
# from gym import Env


@EnvironmentFactory.register("Static_State")
class StaticStateEnvironemnt(EnvironemntProtocol):
    """Environment that operates on set movements between static states"""

    def __init__(self, env_config: json):
        self.environment_map: np.array = env_config["env_map"]

        dimension: int = env_config["map_dimensions"]

        self.max_generation_duration: int = env_config["max_generation_duration"]

        self.start_state: int = env_config["start_location"]

        self.observation_function: callable = partial(
            static_state_observation, ncol=dimension
        )

        self.to_coords_partial: callable = partial(to_coords, ncol=dimension)
        self.to_state_partial: callable = partial(to_state, ncol=dimension)

        self.current_state: int = self.start_state
        self.current_coords: tuple[int, int] = self.to_coords_partial(
            state=self.start_state
        )
        self.curent_step: int = 0
        self.path: list[tuple[int, int]] = []

    def environment_observation(self) -> np.array:
        """Get observation data from the environment"""

        return self.observation_function(self.current_state, self.environment_map)

    def step(self, action: int) -> tuple[int, float, bool, list]:
        """Process the next step/movment in the environment"""

        # Working from here to check if the current state is needed
        self.current_state = self.to_state_partial(coords=self.current_coords)

        reward: float = self.calculate_reward(self.current_coords)
        new_state_x, new_state_y = self.process_action(action)
        termination: bool = self.termination_check(new_state_x, new_state_y)

        info: list = []  # Gym Requiermnt

        self.path.append(new_state_x, new_state_y)
        self.curent_step += 1
        self.current_coords = (new_state_x, new_state_y)

        new_state: int = self.to_state_partial(coords=self.current_coords)

        return new_state, termination, reward, info

        # Update the new state and new state coords a the end

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
            case 0:  # Open Tile
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
            self.curent_step >= self.max_generation_duration,
            get_location_value(self.environment_map, (new_state_x, new_state_y)) == 2,
        ]

        if any(termination_conditions):
            return True

        return False

    def process_action(self, action: int) -> tuple[int]:
        """Process the given action"""

        hrow, hcol = self.current_coords

        # This approach is to be tested - is it cleaner ?
        # holder: dict = {
        #     0: (lambda: hrow - 1, hcol -1),
        #     1: (lambda: hrow - 1, hcol),
        #     2: (lambda: hrow - 1, hcol + 1),
        #     3: (lambda: hrow, hcol -1),
        #     4: (lambda: hrow, hcol),
        #     5: (lambda: hrow, hcol + 1),
        #     6: (lambda: hrow + 1, hcol - 1),
        #     7: (lambda: hrow + 1, hcol),
        #     8: (lambda: hrow + 1, hcol + 1),
        # }

        # update: callable = holder.get[action]
        # new_row, new_col = update()
        # return (new_row, new_col)

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
