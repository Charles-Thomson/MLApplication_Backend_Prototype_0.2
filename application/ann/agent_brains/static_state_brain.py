"""Instance of a brain used by a agent"""
import numpy as np
from ANN.config import config


class BrainInstance:
    """Instance of agent brian"""

    def __init__(
        self,
        brain_id,
        brain_type,
        generation_num,
        hidden_weights,
        output_weights,
        hidden_layer_activation_func,
        output_layer_activation_func,
    ):
        self.brain_type = brain_type  # May rename to Model type ?
        self.brain_id: str = brain_id
        self.generation_num: int = generation_num
        self.hidden_weights: np.array = hidden_weights
        self.output_weights: np.array = output_weights
        self.hidden_layer_activation_func: callable = hidden_layer_activation_func
        self.output_layer_activation_func: callable = output_layer_activation_func
        self.fitness: float = 0.0
        self.traversed_path: list[tuple] = []
        self.fitness_by_step: list[float] = []
        self.svg_path: str = ""
        self.svg_start: str = ""
        self.svg_end: str = ""

    def set_attributes_to_bytes(self) -> None:
        """Covert the np.arrays to bytes for DB storage"""

        self.hidden_weights = self.hidden_weights.tobytes()
        self.output_weights = self.output_weights.tobytes()
        self.traversed_path = ",".join(str(val) for val in self.traversed_path)
        self.fitness_by_step = ",".join(str(val) for val in self.fitness_by_step)

    def get_attributes_from_bytes(self) -> None:
        """Convert the weights from bytes to np.arrays"""

        self.hidden_weights = np.frombuffer(self.hidden_weights).reshape(24, -1)
        self.output_weights = np.frombuffer(self.output_weights).reshape(9, -1)
        self.traversed_path = self.traversed_path.split(",")
        self.fitness_by_step = self.fitness_by_step.split(",")

    def determin_action(self, sight_data: np.array) -> int:
        """Determin best action based on given data/activation"""

        hidden_layer_dot_product = np.dot(sight_data, self.hidden_weights)

        vectorize_func = np.vectorize(self.hidden_layer_activation_func)
        hidden_layer_activation = vectorize_func(hidden_layer_dot_product)

        output_layer_dot_product = np.dot(hidden_layer_activation, self.output_weights)

        return self.output_layer_activation_func(output_layer_dot_product)
