from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


# --- Pydantic Models ---
class AirlineCreate(BaseModel):
    name: str
    code: str
    base_airport_name: str
    employee_count: int

    @validator('employee_count')
    def employee_count_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Employee count must be positive')
        return value

    @validator('code')
    def code_must_be_valid(cls, value):
        if len(value) != 2 or not value.isalpha() or not value.isupper():
            raise ValueError("Airline code must be a two-letter uppercase code")
        return value


class AirlineResponse(BaseModel):
    id: int
    name: str
    code: str
    base_airport_name: str
    employee_count: int
    is_actual: bool
    updated_at: datetime

    class Config:
        orm_mode = True  # Allows creating the model from ORM objects


class AirlineUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    base_airport_name: Optional[str] = None
    employee_count: Optional[int] = None

    @validator('employee_count', always=True)
    def employee_count_must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Employee count must be positive')
        return value

    @validator('code', always=True)
    def code_must_be_valid(cls, value):
        if value is not None and (len(value) != 2 or not value.isalpha() or not value.isupper()):
            raise ValueError("Airline code must be a two-letter uppercase code")
        return value









class AirportCreate(BaseModel):
    name: str
    runway_count: int
    capacity: int

    @validator('runway_count')
    def runway_count_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Runway count must be non-negative')
        return value

    @validator('capacity')
    def capacity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Capacity must be positive')
        return value


class AirportResponse(BaseModel):
    id: int
    name: str
    runway_count: int
    capacity: int
    is_actual: bool
    updated_at: datetime

    class Config:
        orm_mode = True


class AirportUpdate(BaseModel):
    name: Optional[str] = None
    runway_count: Optional[int] = None
    capacity: Optional[int] = None

    @validator('runway_count', always=True)
    def runway_count_must_be_positive(cls, value):
        if value is not None and value < 0:
            raise ValueError('Runway count must be non-negative')
        return value

    @validator('capacity', always=True)
    def capacity_must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Capacity must be positive')
        return value