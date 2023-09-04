"""Hidden layer functions factory"""


class HiddenLayerActvaitionFactory:
    """Factory for hidden layer activaition functions"""

    hidden_layer_activation_functions = {}

    @classmethod
    def get_hidden_activation_func(cls, activation_function):
        """Generate the brain based of given type"""
        try:
            retreval = cls.hidden_layer_activation_functions[activation_function]

        except KeyError as err:
            raise NotImplementedError(f"{activation_function} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.hidden_layer_activation_functions[type_name] = deco_cls
            return deco_cls

        return deco
