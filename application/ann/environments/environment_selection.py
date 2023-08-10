"""Select a given env"""
import json


def new_environment(environemnt_type: str, env_config: json) -> object:
    """Generate a new environemnt based on the given env_config
    var:
        type -> the type of environment
        env_config -> the confieration of the environement

    rtn:
        environemnt instance-> a new environemnt of the given type and configuration
    """

    # This needs to be maintained as new environments are implemented
    environments_available = {
        "static_state_based": "state_based(env_config=env_config)",
        "dynamic_coordiate_based": "coordinate_based(env_config=env_config)"
    }

    return environments_available[environemnt_type]
