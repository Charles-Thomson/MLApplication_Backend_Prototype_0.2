"""Defining the static state environent"""
import json


class Static_State_Environemnt:
    """Environment that operates on set movements between static states"""

    def __init__(self, env_config: json):
        self.env_map = env_config["env_map"]

        self.dimension = env_config["map_dimensions"]

        self.max_generation_duration = env_config["max_generation_duration"]

        self.start_state = env_config["start_location"]
        
        self.current_state = self.start_state
        self.curent_step = 0
        self.path = []