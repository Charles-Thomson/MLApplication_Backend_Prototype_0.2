"""Generator for agent"""
from typing import Generator

from application.ann.agent_brains.brain_factory import BrainFactory

from application.ann.agents.agent_factory import AgentFactory


def new_agent_generator(
    ann_config: dict,
    agent_type: str,
    parents: list,
    max_generation_size: int,
    generation_number: int,
) -> Generator:
    """Test"""
    for _ in range(max_generation_size):
        if generation_number == 0:
            agent_brain: object = BrainFactory.make_brain(
                brain_type="random_weighted_brain",
                ann_config=ann_config,
                parents=parents,
                generation_number=generation_number,
            )
        else:
            agent_brain: object = BrainFactory.make_brain(
                brain_type="generational_weighted_brain",
                ann_config=ann_config,
                parents=parents,
                generation_number=generation_number,
            )

        agent: object = AgentFactory.make_agent(
            agent_type=agent_type, brain=agent_brain
        )

        yield agent
