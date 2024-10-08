from math import sqrt
import numpy as np
from numpy.random import randn, rand

from application.ann.neural_networks.weight_huristics.weight_huristics_factory import (
    WeightHuristicsFactory,
)


@WeightHuristicsFactory.register("he_weight")
def he_weight_init_generator(layer_connections: tuple[int, int]) -> list[float]:
    """HE weight initalization"""
    input_layer_size, output_layer_size = layer_connections

    std = sqrt(2.0 / input_layer_size)
    n = input_layer_size * output_layer_size
    numbers = randn(n)
    scaled = np.round(numbers * std, decimals=3)
    for element in scaled:
        yield element


@WeightHuristicsFactory.register("xavier_weight")
def xavier_weight_init_generator(layer_connections: tuple[int, int]) -> list[float]:
    """xzavier weight initalizations"""
    input_layer_size, output_layer_size = layer_connections

    upper_bounds, lower_bounds = -(1 / sqrt(input_layer_size)), (
        1 / sqrt(input_layer_size)
    )
    n = input_layer_size * output_layer_size
    numbers = rand(n)

    scaled = np.round(
        lower_bounds + numbers * (upper_bounds - lower_bounds), decimals=3
    )
    for element in scaled:
        yield element


@WeightHuristicsFactory.register("normalized_xavier_weight")
def normalized_xavier_weight_init_generator(
    layer_connections: tuple[int, int]
) -> list[float]:
    """normalized xzavier weight initalizations"""
    input_layer_size, output_layer_size = layer_connections
    n = input_layer_size + output_layer_size
    lower_bounds, upper_bounds = -(sqrt(6.0) / sqrt(n)), (sqrt(6.0) / sqrt(n))

    n_numbers = input_layer_size * output_layer_size

    # Numbers
    numbers = rand(n_numbers)
    # Scale numbers to bounds
    scaled = np.round(
        lower_bounds + numbers * (upper_bounds - lower_bounds), decimals=3
    )
    for element in scaled:
        yield element
