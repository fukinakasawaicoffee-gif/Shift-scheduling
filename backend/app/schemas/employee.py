from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: int
    hire_date: Optional[date] = None
    birthday: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    paid_leave_balance: int = 0
    summer_leave_balance: int = 0
    winter_leave_balance: int = 0
    birthday_leave_balance: int = 1


class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    hire_date: Optional[date] = None
    birthday: Optional[date] = None
    paid_leave_balance: Optional[int] = None
    summer_leave_balance: Optional[int] = None
    winter_leave_balance: Optional[int] = None
    birthday_leave_balance: Optional[int] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase):
    id: int
    paid_leave_balance: int
    summer_leave_balance: int
    winter_leave_balance: int
    birthday_leave_balance: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
