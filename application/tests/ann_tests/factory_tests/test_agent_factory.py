import pytest

from application.ann.agents.agent_factory import AgentFactory

from application.ann.agents.static_state_agent import StaticStateMazeAgent


@pytest.mark.parametrize(
    "agent_type, expected_type",
    [("Static_State", StaticStateMazeAgent)],
)
def test_agent_factory(agent_type, expected_type) -> None:
    """Testing the agent factory"""
    test_agent: object = AgentFactory.make_agent(agent_type=agent_type)

    assert isinstance(test_agent, expected_type)
