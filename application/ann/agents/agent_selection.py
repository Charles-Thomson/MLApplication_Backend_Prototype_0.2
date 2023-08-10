"""Select a agent"""


def new_agent(agent_type: str, brain: object) -> object:
    """Generate a new agent based on the given type
    var:
        type -> the type of environment
        brain -> configured brain for the agent

    rtn:
        agent instance -> a new agent of the given type and brain
    
    """

    # This needs to be maintained as new environments are implemented
    agents_available = {
        "static_state_based": "state_based(brain=brain)",
        "dynamic_coordiate_based": "coordinate_based(brain=brain)"
    }

    return agents_available[agent_type]
