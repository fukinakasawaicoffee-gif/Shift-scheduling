from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ShiftRequirement(Base):
    """シフト必要人数モデル - 日付・シフトパターンごとの必要人数"""
    __tablename__ = "shift_requirements"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    shift_pattern_id = Column(Integer, ForeignKey("shift_patterns.id"), nullable=False)

    date = Column(Date, nullable=False, index=True)
    required_count = Column(Integer, nullable=False, default=0)  # 必要人数

    # 特別期間フラグ（セール期間など）
    is_special_period = Column(Boolean, default=False)
    period_name = Column(String)  # 例: "年末セール", "夏季セール"

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション
    department = relationship("Department", back_populates="shift_requirements")
    shift_pattern = relationship("ShiftPattern", back_populates="shift_requirements")
