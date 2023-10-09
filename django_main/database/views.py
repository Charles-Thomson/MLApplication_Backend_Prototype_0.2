from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from django.views.decorators.http import require_http_methods
from database.models import BrainInstanceModel

from database.model_data_handling import brain_instance_to_model


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# TODO NEXT: Import brain instace - may need to refactor file struct
# generate a new brain instacne
# use to bytes
# save the instance
# @require_http_methods(["POST"])
def add_all(request):
    """Add a new Brain Instance"""

    brain_type = "general"
    brain_id = "brain_instance_id_a"
    generation = "generation_number_a"
    hidden_weights = "[5,6,7,8]"
    output_weights = "[5,6,7,8]"
    fitness = "0.5"
    traversed_path = "[2,4,6,8,10]"
    fitness_by_step = "[1.0, 4.0, 6.0 , 10.4, 12.7]"

    new_brain_instance = BrainInstance(
        brain_type=brain_type,
        brain_id=brain_id,
        generation=generation,
        hidden_weights=hidden_weights,
        output_weights=output_weights,
        fitness=fitness,
        traversed_path=traversed_path,
        fitness_by_step=fitness_by_step,
    )

    this_brain = brain_instance_to_model(
        brain_instance=new_brain_instance, model_type="generic"
    )

    new_brain_instance.save()
    return HttpResponse("New instance should be saved")
