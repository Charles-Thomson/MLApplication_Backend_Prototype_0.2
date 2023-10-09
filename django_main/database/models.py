from django.db import models

# from application.ann.agent_brains.brain_factory import BrainInstance

# Create your models here.


class ModelFactory:
    """
    Factory for the generation of models
    """

    model_types: dict = {}

    @classmethod
    def make_model(cls, model_type: str, brain_instance: object):
        """
        Retrive a model of the given type
        var: model_type - the desiered model type
        var: brain_instance - currently not implemented
        """
        try:
            retreval = cls.model_types[model_type]
        except KeyError as err:
            raise NotImplementedError(
                f"Model of type: {model_type} is not implemented"
            ) from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """
        Register a model type
        """

        def deco(deco_cls):
            cls.model_types[type_name] = deco_cls
            return deco_cls

        return deco


# @ModelFactory.register("generic_brain_instance_model")
class BrainInstanceModel(models.Model):
    """
    Generic Brin instance model
    """

    brain_type = models.CharField(max_length=100, default="fit")
    brain_id = models.CharField(max_length=100, default="fit")
    generation = models.CharField(max_length=350)
    fitness = models.CharField(max_length=350)
    traversed_path = models.CharField(max_length=350)
    fitness_by_step = models.CharField(max_length=350)
    hidden_weights = models.BinaryField()
    output_weights = models.BinaryField()

    # TODO: Add the svg elements to the model


# TODO: test for redundancy here - move to the factory approach?


def get_model(model_type: str) -> models.Model:
    """Return a given model -
    Available:
    "generic"
    """

    models: dict[str, models.Model] = {
        "generic": BrainInstanceModel,
    }
    return models[model_type]
