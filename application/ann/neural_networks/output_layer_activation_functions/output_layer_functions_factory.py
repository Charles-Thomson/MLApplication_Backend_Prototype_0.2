"""Output layer functions factory"""


class OutputLayerActvaitionFactory:
    """Factory for output layer activaition functions"""

    output_layer_activation_functions = {}

    @classmethod
    def get_output_activation_func(cls, activation_function):
        """Generate the brain based of given type"""
        try:
            retreval = cls.output_layer_activation_functions[activation_function]

        except KeyError as err:
            raise NotImplementedError(f"{activation_function} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.output_layer_activation_functions[type_name] = deco_cls
            return deco_cls

        return deco
