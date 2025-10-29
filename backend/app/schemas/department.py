from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    max_regular_holidays_per_month: int = 8
    max_consecutive_work_days: int = 6


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    max_regular_holidays_per_month: Optional[int] = None
    max_consecutive_work_days: Optional[int] = None
    is_active: Optional[bool] = None


class Department(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
