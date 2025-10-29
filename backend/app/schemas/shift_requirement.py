from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class ShiftRequirementBase(BaseModel):
    department_id: int
    shift_pattern_id: int
    date: date
    required_count: int
    is_special_period: bool = False
    period_name: Optional[str] = None


class ShiftRequirementCreate(ShiftRequirementBase):
    pass


class ShiftRequirementUpdate(BaseModel):
    required_count: Optional[int] = None
    is_special_period: Optional[bool] = None
    period_name: Optional[str] = None


class ShiftRequirement(ShiftRequirementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
