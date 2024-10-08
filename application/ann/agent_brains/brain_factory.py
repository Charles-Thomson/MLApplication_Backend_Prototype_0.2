"""Brain generation in the form of a factory"""
from __future__ import annotations
from copy import deepcopy
import random
import uuid
import numpy as np


from application.ann.agent_brains.static_state_brain import BrainInstance


class BrainFactory:
    """Factory for generations fo brains"""

    brain_types = {}

    @classmethod
    def make_brain(
        cls,
        current_generation_number: int,
        brain_type,
        ann_config: dict,
        parents: list[BrainInstance],
    ):
        """Generate the brain based of given type"""
        try:
            retreval = cls.brain_types[brain_type]

        except KeyError as err:
            raise NotImplementedError(f"{brain_type} Not implemented") from err

        return retreval(
            current_generation_number=current_generation_number,
            ann_config=ann_config,
            parents=parents,
        )

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.brain_types[type_name] = deco_cls
            return deco_cls

        return deco


def generate_brain_id() -> str:
    """Generate a random brain_ID"""
    brain_id = uuid.uuid4()
    brain_id = str(brain_id)[:10]
    return brain_id


@BrainFactory.register("generational_weighted_brain")
def new_generational_weighted_brain(
    ann_config: dict, parents: list[BrainInstance], current_generation_number
) -> BrainInstance:
    """Generate a new generationally weighted brain"""

    MUTATION_THRESHOLD: int = 50

    new_generation_function: callable = ann_config["new_generation_func"]

    val: int = len(parents)
    weightings: list[float] = tuple(val / i for i in range(1, val + 1))

    parent_a, parent_b = random.choices(parents, weights=weightings, k=2)

    parent_a: BrainInstance = deepcopy(parent_a)
    parent_b: BrainInstance = deepcopy(parent_b)

    new_input_to_hidden_weight: np.array = new_generation_function(
        parent_a.hidden_weights, parent_b.hidden_weights
    )

    new_hidden_to_output_weights: np.array = new_generation_function(
        parent_a.output_weights, parent_b.output_weights
    )

    if random.randint(0, 100) > MUTATION_THRESHOLD:
        random_selection = random.randint(0, 1)
        if random_selection == 0:
            new_input_to_hidden_weight = apply_mutation(new_input_to_hidden_weight)

        if random_selection == 1:
            new_hidden_to_output_weights = apply_mutation(new_hidden_to_output_weights)

    ann_config["hidden_weights"] = new_input_to_hidden_weight
    ann_config["output_weights"] = new_hidden_to_output_weights

    ann_config["brain_id"] = generate_brain_id()

    return BrainInstance(
        brain_config=ann_config,
        current_generation_number=current_generation_number,
    )


def apply_mutation(weight_set: np.array) -> np.array:
    """Apply a +/- 10% mutation to the weights to give variance"""

    weight_set_shape: tuple = weight_set.shape

    # select random weight from set

    x_loc: int = random.randrange(weight_set_shape[0])
    y_loc: int = random.randrange(weight_set_shape[1])

    weight_to_mutate: float = weight_set[x_loc][y_loc]

    mutation_amount: int = random.randint(1, 10)
    positive_mutation: float = weight_to_mutate - (weight_to_mutate / mutation_amount)
    negitive_mutation: float = weight_to_mutate + (weight_to_mutate / mutation_amount)

    mutation: float = random.choice((positive_mutation, negitive_mutation))

    weight_set[x_loc][y_loc] = mutation

    return weight_set


@BrainFactory.register("random_weighted_brain")
def new_random_weighted_brain(
    current_generation_number: int, ann_config: dict, parents: list
) -> BrainInstance:
    """Generate a randomly weighted brain"""

    hidden_weights: np.array = initialize_weights(
        layer_connections=ann_config["input_to_hidden_connections"],
        weight_heuristic=ann_config["weight_init_huristic"],
    )

    output_weights: np.array = initialize_weights(
        layer_connections=ann_config["hidden_to_output_connections"],
        weight_heuristic=ann_config["weight_init_huristic"],
    )

    ann_config["hidden_weights"] = hidden_weights
    ann_config["output_weights"] = output_weights

    ann_config["brain_id"] = generate_brain_id()

    return BrainInstance(
        current_generation_number=current_generation_number,
        brain_config=ann_config,
    )


def initialize_weights(
    layer_connections: tuple[int, int], weight_heuristic: callable
) -> np.array:
    """Generate random weigths between to layers of a specified sizes"""

    # may clean up to return the set weight size not 500

    get_weight = weight_heuristic(layer_connections)

    sending_layer, reciving_layer = layer_connections
    rand_weights: np.array = np.array(
        [
            [next(get_weight) for i in range(reciving_layer)]
            for i in range(sending_layer)
        ]
    )

    return rand_weights
