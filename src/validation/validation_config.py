from pydantic import BaseModel, Field, model_validator
from typing import Union
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s-%(asctime)s-%(message)s')
logger= logging.getLogger(__name__)

class budgetValidation(BaseModel): 
    limit_budget: Union[int, float] = Field(gt=0)
    minimum_budget: Union[int, float] = Field(ge=0)
    
    @model_validator(mode='after')
    def minmun_maxim_validation(self): 
        limit= self.limit_budget
        minim= self.minimum_budget
        
        if minim > limit: 
            logger.error(f'The minimum {minim} cannot be greater to the maximum {limit}')
            raise ValueError(f'The minimum {minim} cannot be greater to the maximum {limit}')
        
        return self

class timesValidation(BaseModel): 
    time_limit_of_inactive_server: int = Field(ge=0)
    maximum_time_to_postpone: int = Field(ge=0)
    minimum_time_to_postpone: int = Field(ge=0)
    
    @model_validator(mode='after')
    def minimun_maxim_validation(self): 
        maxim= self.maximum_time_to_postpone
        minim= self.minimum_time_to_postpone
        
        if minim > maxim: 
            logger.error(f'The minimum {minim} cannot be greater to the maximum {maxim}')
            raise ValueError(f'The minimum {minim} cannot be greater to the maximum {maxim}')
        
        return self

class validation_config(BaseModel): 
    budget: budgetValidation
    times: timesValidation

