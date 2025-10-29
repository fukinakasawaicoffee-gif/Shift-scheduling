from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Department(Base):
    """部署モデル"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)

    # 休日設定
    max_regular_holidays_per_month = Column(Integer, default=8)  # 月の通常休日数
    max_consecutive_work_days = Column(Integer, default=6)  # 最大連続勤務日数

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション
    employees = relationship("Employee", back_populates="department")
    shift_patterns = relationship("ShiftPattern", back_populates="department")
    shift_requirements = relationship("ShiftRequirement", back_populates="department")
