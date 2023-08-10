"""Select a given env"""
import json


def new_brain(brain_type: str, ann_config: json) -> object:
    """Generate a new environemnt based on the given ann_config
    var:
        type -> the type of environment
        env_config -> the confieration of the environement

    rtn:
        brain instance -> a new environemnt of the given type and configuration
    
    """

    # This needs to be maintained as new environments are implemented
    brains_available = {
        "static_state_based": "state_based(ann_config=ann_config)",
        "dynamic_coordiate_based": "coordinate_based(ann_config=ann_config)"
    }

    return brains_available[brain_type]
