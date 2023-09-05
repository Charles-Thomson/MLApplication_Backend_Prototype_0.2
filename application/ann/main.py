from neural_networks.weight_huristics.weight_huristics_factory import (
    WeightHuristicsFactory,
)


class TestFactory:
    """Factory for weight huristics activaition functions"""

    Test_funcs = {}

    @classmethod
    def get_huristic(cls, weight_huristic: str):
        """Get weight huristic of given type"""
        print(cls.Test_funcs)
        try:
            retreval = cls.Test_funcs[weight_huristic]

        except KeyError as err:
            raise NotImplementedError(f"{weight_huristic} Not implemented") from err

        return retreval()

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.Test_funcs[type_name] = deco_cls
            return deco_cls

        return deco


@TestFactory.register("test_print")
def test_function():
    return lambda: print("test function")


def basic_test():
    """Testing stuff"""

    test = WeightHuristicsFactory.get_huristic("he_weight")

    print(test)


basic_test()
