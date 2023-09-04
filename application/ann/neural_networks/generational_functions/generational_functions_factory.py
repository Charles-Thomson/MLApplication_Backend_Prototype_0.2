"""generational functions factory"""


class GenerationalFunctionsFactory:
    """Factory for geerational functions"""

    generational_functions = {}

    @classmethod
    def get_generation_func(cls, generational_funcation):
        """Generate the brain based of given type"""
        try:
            retreval = cls.generational_functions[generational_funcation]

        except KeyError as err:
            raise NotImplementedError(
                f"{generational_funcation} Not implemented"
            ) from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.generational_functions[type_name] = deco_cls
            return deco_cls

        return deco
