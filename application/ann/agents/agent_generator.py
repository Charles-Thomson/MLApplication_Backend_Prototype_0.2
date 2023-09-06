"""Generator for agent"""
from typing import Generator

from application.ann.agent_brains.brain_factory import BrainFactory

from application.ann.agents.agent_factory import AgentFactory


def new_agent_generator(
    ann_config: dict,
    agent_type: str,
    parents: list,
    max_generation_size: int,
    current_generation_number: int,
    environment: object,
) -> Generator:
    """Test"""
    for _ in range(max_generation_size):
        this_brain_type = "generational_weighted_brain"

        if current_generation_number == 0:
            this_brain_type = "random_weighted_brain"

        agent_brain: object = BrainFactory.make_brain(
            brain_type=this_brain_type,
            ann_config=ann_config,
            parents=parents,
            current_generation_number=current_generation_number,
        )

        agent: object = AgentFactory.make_agent(
            agent_type=agent_type, brain=agent_brain, environment=environment
        )

        yield agent
