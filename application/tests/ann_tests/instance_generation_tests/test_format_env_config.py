# """Testing the setiing of the envrionment config in the instance generation file"""
# import numpy as np

# from application.ann.instance_generation.instance_generation_main import (
#     format_env_config,
# )


# def test_format_env_config() -> None:
#     """Test the formatting of the given data to the correct env data format"""

#     test_config = {
#         "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
#         "map_dimensions": "4",
#         "start_location": "1,1",
#         "max_number_of_genrations": "2",
#         "max_generation_size": "2",
#         "fitness_threshold": "2",
#         "new_generation_threshold": "2",
#     }
#     formatted_config: dict = format_env_config(test_config)

#     assert isinstance(formatted_config["env_map"], np.ndarray)
#     assert isinstance(formatted_config["map_dimensions"], int)
#     assert isinstance(formatted_config["start_location"], tuple)
#     assert isinstance(formatted_config["max_number_of_genrations"], int)
#     assert isinstance(formatted_config["max_generation_size"], int)
#     assert isinstance(formatted_config["fitness_threshold"], float)
#     assert isinstance(formatted_config["new_generation_threshold"], int)
