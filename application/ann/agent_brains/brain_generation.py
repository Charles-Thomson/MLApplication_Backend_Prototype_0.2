"""Brain generation in the form of a factory"""

from typing import final
import numpy as np


INPUT_LAYER_SIZE: final = 24
INPUT_TO_HIDDEN_CONNECTIONS: final = (24, 9)
HIDDEN_TO_OUTPUT_CONNECTIONS: final = (9, 9)


class BrainFactory:
    """Factory for generations fo brains"""

    brain_types = {}

    @classmethod
    def make_brain(cls, brain_type):
        """Generate the brain based of given type"""
        try:
            retreval = cls.brain_types[brain_type]

        except KeyError as err:
            raise NotImplementedError(f"{brain_type} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.envs[type_name] = deco_cls
            return deco_cls

        return deco
