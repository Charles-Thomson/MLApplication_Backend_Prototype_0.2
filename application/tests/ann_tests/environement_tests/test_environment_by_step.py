"""Testing the configuation of an enviroment once it hs been created"""

import numpy as np


from application.ann.environments.environment_factory import (
    StaticStateEnvironemnt,
)

from application.ann.environments.environment_factory import (
    EnvironmentFactory,
)

from application.ann.instance_generation.instance_generation_main import (
    format_env_config,
)

# 1,1,1,1
# 1,1,3,1
# 1,1,1,1
# 1,1,1,1


test_config = {
    "env_map": "1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,1",
    "map_dimensions": "4",
    "start_location": "1,1",
    "max_number_of_genrations": "2",
    "max_generation_size": "2",
    "fitness_threshold": "2",
    "new_generation_threshold": "2",
}

test_env_type: str = "Static_State"


def test_environment_step_by_step():
    """Testing the environment per step by step"""

    env_config: dict = format_env_config(test_config)
    static_state_test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
        test_env_type, config=env_config
    )

    assert static_state_test_env.start_coords == (1, 1)
    assert static_state_test_env.current_coords == (1, 1)
    assert static_state_test_env.current_step == 0

    test_action = 5  # move left
    new_coords_a, termination_a, reward_a = static_state_test_env.step(test_action)

    print(new_coords_a, termination_a, reward_a, "Step 1")

    assert new_coords_a == (1, 2)
    assert termination_a == False
    assert reward_a == 0.15

    new_coords_b, termination_b, reward_b = static_state_test_env.step(test_action)

    # # TODO: Error in the reward value when landing on goal node - returning 0.0 - should return 3
    print(new_coords_b, termination_b, reward_b, "step 2")

    assert new_coords_b == (1, 3)
    assert termination_b == False
    assert reward_b == 3.0
