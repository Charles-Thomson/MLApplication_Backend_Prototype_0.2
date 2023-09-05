"""weight huristics functions factory"""


class WeightHuristicsFactory:
    """Factory for weight huristics activaition functions"""

    weight_huristics_functions = {}

    @classmethod
    def get_huristic(cls, weight_huristic: str):
        """Get weight huristic of given type"""
        try:
            retreval = cls.weight_huristics_functions[weight_huristic]

        except KeyError as err:
            raise NotImplementedError(f"{weight_huristic} Not implemented") from err

        return retreval()

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.weight_huristics_functions[type_name] = deco_cls
            return deco_cls

        return deco
