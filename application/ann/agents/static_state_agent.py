"""Static state agent type"""

# define the custom type of brain

from application.ann.agents.agent_factory import AgentFactory


@AgentFactory.register_agent("Static_State")
class StaticStateMazeAgent:
    """Static state maze agent"""

    def __init__(self, environemnt: object, agent_brain: object):
        self.environment: object = environemnt
        self.brain: object = agent_brain

        self.path: list[int] = []
        self.fitness_by_step: list[tuple] = []
        self.fitness: float = 0.0
        self.termination: bool = False

    def run_agent(self) -> object:
        """Run the agent throught the environment"""

        while self.termination is False:
            observation_data = self.environment.get_environment_observation()
            action = self.brain.determin_action(observation_data)

            new_coords, termination_status, reward = self.environment.step(action)

            self.path.append(new_coords)
            self.termination = termination_status
            self.fitness += reward
            self.fitness_by_step.append(self.fitness)

        self.set_brain_data()

        return self.brain

    def set_brain_data(self) -> None:
        """Update the brain data once termination is reached"""
        self.brain.fitness = self.fitness
        self.brain.traversed_path = self.path
        self.brain.fitness_by_step = self.fitness_by_step
