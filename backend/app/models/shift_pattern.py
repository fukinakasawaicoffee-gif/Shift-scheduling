from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ShiftType(str, enum.Enum):
    """シフトタイプ"""
    EARLY = "early"  # 早番
    NORMAL = "normal"  # 普通番
    LATE = "late"  # 遅番
    NIGHT = "night"  # 夜勤
    OTHER = "other"  # その他


class ShiftPattern(Base):
    """シフトパターンモデル - 部署ごとの勤務パターン"""
    __tablename__ = "shift_patterns"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    name = Column(String, nullable=False)  # 例: "早番A", "早番B"
    code = Column(String, nullable=False)  # 例: "EA", "EB"
    shift_type = Column(SQLEnum(ShiftType), nullable=False)

    start_time = Column(Time, nullable=False)  # 開始時刻
    end_time = Column(Time, nullable=False)  # 終了時刻
    work_hours = Column(Integer, nullable=False)  # 勤務時間（分）

    # 色分けなどUI用
    color_code = Column(String)  # 例: "#FF5733"

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション
    department = relationship("Department", back_populates="shift_patterns")
    schedules = relationship("Schedule", back_populates="shift_pattern")
    shift_requirements = relationship("ShiftRequirement", back_populates="shift_pattern")
