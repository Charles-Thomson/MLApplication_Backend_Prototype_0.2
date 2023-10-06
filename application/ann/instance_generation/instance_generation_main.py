"""generate the intances for trainning of the ann"""
import json
from typing import Generator
import uuid

from functools import partial

from application.ann.environments.environment_factory import EnvironmentFactory

from application.ann.agents.agent_generator import new_agent_generator

from application.ann.instance_generation.config_formatting import (
    format_instance_config,
    format_ann_config,
    format_env_config,
)

from application.ann.logging_files.logging_deco import (
    with_brain_logging,
    with_fitness_threshold_logging,
)


# TODO: Implement ref to movement i.e 0 = UL , 1 = U ect ect

# TODO: Instance generation:
# Need to save the highest fitness brain from each instance run


# TODO: Set up the Django DB model to store the highest fitness from each instance


class Learning_Instance:
    """
    The generated instance class
    The running of this instance will result in a "Trained" Brain that can
    then be used on a new environment
    """

    def __init__(self, id, agent_generator: object, instance_config: dict):
        self.instance_id: str = id

        self.current_fitness_threshold: float = instance_config["fitness_threshold"]
        self.current_generation_failure_threshold = 2

        self.max_number_of_generations: int = instance_config[
            "max_number_of_genrations"
        ]

        self.max_generation_size: int = instance_config["max_generation_size"]
        self.agent_generator: callable = agent_generator  # new per generation

        self.current_parents: list = []

        self.new_generation_threshold: int = instance_config["new_generation_threshold"]

        self.brains = []

    def run_instance(self):
        """run the instance"""
        current_generation_number: int = 0
        # new_fitness_threshold = self.current_fitness_threshold
        new_parents: list = []

        for current_generation_number in range(self.max_number_of_generations):
            new_fitness_threshold = self.generate_new_fitness_threshold(new_parents)

            agent_generator: object = self.agent_generator(
                parents=new_parents,
                max_generation_size=self.max_generation_size,
                current_generation_number=current_generation_number,
            )

            new_parents = self.run_generation(
                agent_generator=agent_generator,
                fitness_threshold=new_fitness_threshold,
            )

            if len(new_parents) <= self.current_generation_failure_threshold:
                break

        # For logging deco
        return self.brains

    def run_generation(
        self, agent_generator: Generator, fitness_threshold: float
    ) -> None:
        """
        Run a new generation
        var: agent_generator
        rtn: new_parents - A list of brain instances tha pass the fitnees threshold
        """
        new_parents: list = []

        for _ in range(self.max_generation_size):
            agent = next(agent_generator)
            post_run_agent_brain: object = agent.run_agent()

            self.brains.append(post_run_agent_brain)  # for logging

            if post_run_agent_brain.fitness >= fitness_threshold:
                new_parents.append(post_run_agent_brain)

            if len(new_parents) >= self.new_generation_threshold:
                break

        return new_parents

    # TODO: Move fitness threshold logging to the testing side
    @with_fitness_threshold_logging
    def generate_new_fitness_threshold(self, parents: list[object]) -> float:
        """
        Calculate a new fitness threshold based on the average fitness + 10%
        of the given parents fitness
        """

        if not parents:
            return 2.0

        fitness_average: float = sum(instance.fitness for instance in parents) / len(
            parents
        )

        # * 10 -> inc threshold by 10%
        return fitness_average + (fitness_average / 100) * 10


def new_instance(config: json) -> Learning_Instance:
    """Generate a new instance based on the given config settings
    var: config - the given config settings as json
    rtn: Callable object
    """

    env_config: dict = format_env_config(config["env_config"])

    ann_config_formatted: dict = format_ann_config(config["ann_config"])

    instance_config_formatted: dict = format_instance_config(config["instance_config"])

    environment: object = EnvironmentFactory.make_env(
        env_type=config["env_type"], config=env_config
    )

    agent_generater: callable = partial(
        new_agent_generator,
        ann_config=ann_config_formatted,
        agent_type=config["agent_type"],
        environment=environment,
    )

    id: str = generate_instance_id()

    this_instance = Learning_Instance(
        id=id,
        agent_generator=agent_generater,
        instance_config=instance_config_formatted,
    )

    return this_instance


def generate_instance_id() -> str:
    """Generate a random brain_ID"""
    brain_id = uuid.uuid4()
    brain_id = str(brain_id)[:10]
    return brain_id
