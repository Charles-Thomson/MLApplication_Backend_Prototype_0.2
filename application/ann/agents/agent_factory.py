"""Agent generation Factory"""


class AgentFactory:
    """Factory for agent selection"""

    agents = {}

    @classmethod
    def make_agent(cls, agent_type, brain):
        """Generate the agent based on given type"""
        try:
            retreval = cls.agents[agent_type]
        except KeyError as err:
            raise NotImplementedError(f"{agent_type} is not implemented") from err

        return retreval(brain=brain)

    @classmethod
    def register_agent(cls, agent_type):
        """Decorator to register the agent type"""

        def deco(deco_cls):
            cls.agents[agent_type] = deco_cls
            return deco_cls

        return deco
