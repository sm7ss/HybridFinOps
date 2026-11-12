from pydantic import BaseModel, Field
from typing import Union

class budgetValidation(BaseModel): 
    limit_budget: Union[int, float] = Field(gt=0)
    minimum_budget: Union[int, float] = Field(gt=0)

class timesValidation(BaseModel): 
    time_limit_of_inactive_server: int = Field(ge=0)
    minimum_time_to_postpone: int = Field(ge=0)
    maximum_time_to_postpone: int = Field(ge=0)

class validation(BaseModel): 
    budget: budgetValidation
    times: timesValidation

