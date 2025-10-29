from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Employee(Base):
    """従業員モデル"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    # 部署
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    # 雇用情報
    hire_date = Column(Date)
    birthday = Column(Date)  # バースデー休暇用

    # 有給・特別休暇の残日数
    paid_leave_balance = Column(Integer, default=0)  # 有給残日数
    summer_leave_balance = Column(Integer, default=0)  # 夏季休暇残日数
    winter_leave_balance = Column(Integer, default=0)  # 冬季休暇残日数
    birthday_leave_balance = Column(Integer, default=1)  # バースデー休暇残日数

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション
    department = relationship("Department", back_populates="employees")
    schedules = relationship("Schedule", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
