from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class ScheduleBase(BaseModel):
    employee_id: int
    shift_pattern_id: Optional[int] = None
    date: date
    is_holiday: bool = False
    holiday_type: Optional[str] = None
    notes: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    shift_pattern_id: Optional[int] = None
    is_holiday: Optional[bool] = None
    holiday_type: Optional[str] = None
    notes: Optional[str] = None
    is_confirmed: Optional[bool] = None
    is_published: Optional[bool] = None


class Schedule(ScheduleBase):
    id: int
    is_confirmed: bool
    is_published: bool
    generated_by_system: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GenerateScheduleRequest(BaseModel):
    """シフト自動生成リクエスト"""
    department_id: int
    start_date: date
    end_date: date
    time_limit_seconds: int = 300


class GenerateScheduleResponse(BaseModel):
    """シフト自動生成レスポンス"""
    success: bool
    message: str
    schedules_created: int
    statistics: dict
