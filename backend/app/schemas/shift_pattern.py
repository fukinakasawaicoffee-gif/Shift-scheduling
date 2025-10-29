from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
from app.models.shift_pattern import ShiftType


class ShiftPatternBase(BaseModel):
    department_id: int
    name: str
    code: str
    shift_type: ShiftType
    start_time: time
    end_time: time
    work_hours: int
    color_code: Optional[str] = None


class ShiftPatternCreate(ShiftPatternBase):
    pass


class ShiftPatternUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    shift_type: Optional[ShiftType] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    work_hours: Optional[int] = None
    color_code: Optional[str] = None
    is_active: Optional[bool] = None


class ShiftPattern(ShiftPatternBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
