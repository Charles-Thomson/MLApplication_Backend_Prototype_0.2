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

from application.ann.logging_files.logging_deco import (
    with_brain_logging,
    with_fitness_threshold_logging,
)


class Learning_Instance:
    """
    The generated instance class
    The running of this instance will result in a "Trained" Brain that can
    then be used on a new environment
    """

    def __init__(self, id, agent_generator: object, instance_config: dict):
        self.instance_id: str = id

        self.current_fitness_threshold: float = instance_config["fitness_threshold"]

        self.max_number_of_generations: int = instance_config[
            "max_number_of_genrations"
        ]

        self.max_generation_size: int = instance_config["max_generation_size"]
        self.agent_generator: callable = agent_generator  # new per generation

        self.current_parents: list = []
        self.new_parents: list = []

        self.new_generation_threshold: int = instance_config["new_generation_threshold"]

        self.brains = []

    def run_instance(self):
        """run the instance"""
        current_generation_number: int = 0
        current_generation_size: int = 0

        while current_generation_number < self.max_number_of_generations:
            agent_generator: object = self.agent_generator(
                parents=self.current_parents,
                max_generation_size=self.max_generation_size,
                current_generation_number=current_generation_number,
            )

            current_generation_size = 0
            print("new generation starting")

            # break this ot to func ?
            while current_generation_size < self.max_generation_size:
                agent = next(agent_generator)
                post_run_agent_brain: object = agent.run_agent()

                self.brains.append(post_run_agent_brain)  # for logging testing

                if post_run_agent_brain.fitness >= self.current_fitness_threshold:
                    self.new_parents.append(post_run_agent_brain)

                if len(self.new_parents) >= self.new_generation_threshold:
                    self.current_parents = self.new_parents
                    self.new_parents = []
                    self.set_new_fitness_threshold()
                    print("new generation")
                    break

                current_generation_size += 1

            current_generation_number += 1

        print(
            f"SYSTEM - COMPLETED RUN - Generation Reached: {current_generation_number}"
        )

        # For logging deco
        return self.brains

    @with_fitness_threshold_logging
    def set_new_fitness_threshold(self) -> float:
        """
        Calculate a new fitness threshold based on the average fitness + 10%
        of the given parents fitness
        """
        parents: list = self.current_parents
        fitness_threshold_percentage_growth: float = 10

        total_combined_fitness: float = sum(instance.fitness for instance in parents)
        fitness_average: float = total_combined_fitness / len(parents)

        new_fitness_threshold: float = (
            fitness_average
            + (fitness_average / 100) * fitness_threshold_percentage_growth
        )

        self.current_fitness_threshold = new_fitness_threshold

        # For logging deco
        return new_fitness_threshold


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
