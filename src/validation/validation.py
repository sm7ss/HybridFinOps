from .validation_config import validation_config
from .validation_env import validation_env

from pydantic import BaseModel

class validation(BaseModel): 
    config_val: validation_config
    env_val: validation_env


