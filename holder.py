# from django.db import models

# # from application.ann.agent_brains.brain_factory import BrainInstance

# # Create your models here.


# class ModelFactory:
#     """
#     Factory for the generation of models
#     """

#     model_types: dict = {}

#     @classmethod
#     def make_model(cls, model_type: str, brain_instance: object):
#         """
#         Retrive a model of the given type
#         var: model_type - the desiered model type
#         var: brain_instance - currently not implemented
#         """
#         try:
#             retreval = cls.model_types[model_type]
#         except KeyError as err:
#             raise NotImplementedError(
#                 f"Model of type: {model_type} is not implemented"
#             ) from err

#         return retreval

#     @classmethod
#     def register(cls, type_name):
#         """
#         Register a model type
#         """

#         def deco(deco_cls):
#             cls.model_types[type_name] = deco_cls
#             return deco_cls

#         return deco


# @ModelFactory.register("generic_brain_instance_model")
# class BrainInstanceModel(models.Model):
#     """
#     Generic Brin instance model
#     """

#     brain_type = models.CharField(max_length=100, default="fit")
#     brain_id = models.CharField(max_length=100, default="fit")
#     generation = models.CharField(max_length=350)
#     fitness = models.CharField(max_length=350)
#     traversed_path = models.CharField(max_length=350)
#     fitness_by_step = models.CharField(max_length=350)
#     hidden_weights = models.BinaryField()
#     ouput_weights = models.BinaryField()

#     # TODO: Add the svg elements to the model


# # TODO: test for redundancy here - move to the factory approach?


# def get_model(model_type: str) -> models.Model:
#     """Return a given model -
#     Available:
#     "generic"
#     """

#     models: dict[str, models.Model] = {
#         "generic": BrainInstanceModel,
#     }
#     return models[model_type]


# # TODO: Test factory approach after DB implmented
# from application.web_app.models import get_model
# from application.ann.agent_brains.brain_factory import BrainInstance


# def brain_instance_to_model(brain_instance: object, model_type: str) -> BrainInstance:
#     """Save the brain instance as a fit instance"""

#     model = get_model(model_type=model_type)

#     brain_instance.set_attributes_to_bytes()

#     new_db_brain_model = model(
#         brain_id=brain_instance.brain_id,
#         brain_type=brain_instance.brain_type,  # May rename to Model type ?
#         generation_num=brain_instance.generation_num,
#         hidden_weights=brain_instance.hidden_weights,
#         output_weights=brain_instance.output_weights,
#         fitness=brain_instance.fitness,
#         traversed_path=brain_instance.traversed_path,
#         fitness_by_step=brain_instance.fitness_by_step,
#     )

#     return new_db_brain_model


# def model_to_brain_instance(brain_model: BrainInstance) -> BrainInstance:
#     """Convert a brain_model used by the DB to a Brain Instance"""

#     new_brain_instace: BrainInstance = BrainInstance(
#         brain_id=brain_model.brain_id,
#         brain_type=brain_model.brain_type,
#         generation_num=brain_model.generation_num,
#         hidden_weights=brain_model.hidden_weights,
#         output_weights=brain_model.output_weights,
#         fitness=brain_model.fitness,
#         traversed_path=brain_model.traversed_path,
#         fitness_by_step=brain_model.fitness_by_step,
#     )

#     return new_brain_instace
