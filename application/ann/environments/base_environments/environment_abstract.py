"""The abstract for base environments"""
from typing import Protocol
from abc import abstractmethod


class EnvironemntProtocol(Protocol):
    """The environemtn protocol"""

    @abstractmethod
    def print_id() -> None:
        raise NotImplementedError


class EnvironmentFactory:
    """Factory class fot environments"""

    envs = {}

    @classmethod
    def make_env(cls, env_type: str):
        """Make the env based on given version"""
        try:
            retreval = cls.envs[env_type]
        except KeyError as err:
            raise NotImplementedError(f"{env_type} is not implemented") from err
        
        retreval.print_id()
        # return retreval

    @classmethod
    def register(cls, type_name):
        def deco(deco_cls):
            cls.envs[type_name] = deco_cls
            return deco_cls
        return deco






@EnvironmentFactory.register("env_1")
class env_1(EnvironemntProtocol):
    """test of the metaprogramming with protocols """

    def print_id() -> None:
        print("env_1 called")


@EnvironmentFactory.register("env_2")
class env_2(EnvironemntProtocol):
    """test of the metaprogramming with protocols """

    def print_id() -> None:
        print("env_2 called")
    

EnvironmentFactory.make_env("env_2")

