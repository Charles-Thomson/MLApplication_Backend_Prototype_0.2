"""generate the intances for trainning of the ann"""
import json
import uuid

from functools import partial

from application.ann.environments.environment_types.environment_factory import (
    EnvironmentFactory,
)

from application.ann.agents.agent_generator import new_agent_generator

from application.ann.instance_generation.config_formatting import (
    format_instance_config,
    format_ann_config,
    format_env_config,
)

from application.ann.logging_files.logging_deco import with_brain_logging


class Learning_Instance:
    """
    The generated instance class
    """

    def __init__(
        self, id, environment: object, agent_generator: object, instance_config: dict
    ):
        self.instance_id: str = id
        # self.environment: object = environment
        self.memeory = []  # this will be converted into a db model
        self.current_generation_number: int = 0
        self.current_generation_size: int = 0

        self.fitness_threshold: float = instance_config["fitness_threshold"]
        self.max_number_of_generations: int = instance_config[
            "max_number_of_genrations"
        ]
        self.new_generation_threshold: int = instance_config["new_generation_threshold"]
        self.max_generation_size: int = instance_config["max_generation_size"]
        self.max_number_of_generations: int = 1  # Need to implement this
        self.agent_generator: callable = agent_generator  # new per generation
        self.parents = []
        self.brains = []

    @with_brain_logging
    def run_instance(self):
        """run the instance"""

        while self.current_generation_number < self.max_number_of_generations:
            agent_generator: object = self.agent_generator(
                parents=self.parents,
                max_generation_size=self.max_generation_size,
                current_generation_number=self.current_generation_number,
            )

            while self.current_generation_size < self.max_generation_size:
                agent = next(agent_generator)
                post_run_agent_brain: object = agent.run_agent()

                self.memeory.append(post_run_agent_brain)
                self.brains.append(post_run_agent_brain)

                self.current_generation_size += 1

            self.current_generation_number += 1

        print(self.brains)

        return self.brains


def new_instance(config: json) -> Learning_Instance:
    """Generate a new instance based on the given config settings
    var: config - the given config settings as json
    rtn: Callable object
    """

    print("in new insance")

    env_config: dict = format_env_config(config["env_config"])

    ann_config_formatted: dict = format_ann_config(config["ann_config"])

    instance_config_formatted: dict = format_instance_config(config["instance_config"])

    environment: object = EnvironmentFactory.make_env(
        env_type=config["env_type"], config=env_config
    )

    print("vars generated")

    agent_generater: callable = partial(
        new_agent_generator,
        ann_config=ann_config_formatted,
        agent_type=config["agent_type"],
        environment=environment,
    )

    id: str = generate_instance_id()

    this_instance = Learning_Instance(
        id=id,
        environment=environment,
        agent_generator=agent_generater,
        instance_config=instance_config_formatted,
    )

    print(this_instance)

    return this_instance


def generate_instance_id() -> str:
    """Generate a random brain_ID"""
    brain_id = uuid.uuid4()
    brain_id = str(brain_id)[:10]
    return brain_id
