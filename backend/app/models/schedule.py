from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey, Boolean, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Schedule(Base):
    """スケジュール（シフト割り当て）モデル"""
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_pattern_id = Column(Integer, ForeignKey("shift_patterns.id"), nullable=True)  # Nullの場合は休日

    date = Column(Date, nullable=False, index=True)

    # 休日の場合のタイプ
    is_holiday = Column(Boolean, default=False)
    holiday_type = Column(String)  # "regular", "paid_leave", "summer_leave", "winter_leave", "birthday_leave"

    # ステータス
    is_confirmed = Column(Boolean, default=False)  # 確定済みかどうか
    is_published = Column(Boolean, default=False)  # 公開済みかどうか

    # メモ
    notes = Column(Text)

    # 生成情報
    generated_by_system = Column(Boolean, default=False)  # システムによる自動生成かどうか

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション
    employee = relationship("Employee", back_populates="schedules")
    shift_pattern = relationship("ShiftPattern", back_populates="schedules")
