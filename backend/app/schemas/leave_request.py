from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.leave_request import LeaveType, LeaveRequestStatus


class LeaveRequestBase(BaseModel):
    employee_id: int
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: Optional[str] = None
    notes: Optional[str] = None


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestUpdate(BaseModel):
    leave_type: Optional[LeaveType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[LeaveRequestStatus] = None


class LeaveRequest(LeaveRequestBase):
    id: int
    status: LeaveRequestStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
