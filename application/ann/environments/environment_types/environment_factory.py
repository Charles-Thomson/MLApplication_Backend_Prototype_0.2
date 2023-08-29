"""The factory for the environments"""


class EnvironmentFactory:
    """Factory class fot environments"""

    envs = {}

    @classmethod
    def make_env(cls, env_type: str, config: dict):
        """Make the env based on given version"""
        try:
            retreval = cls.envs[env_type]
        except KeyError as err:
            raise NotImplementedError(f"{env_type} is not implemented") from err

        # retreval.print_id()
        return retreval(env_config=config)

    @classmethod
    def register(cls, type_name):
        """Register an env to the factory"""

        def deco(deco_cls):
            cls.envs[type_name] = deco_cls
            return deco_cls

        return deco
