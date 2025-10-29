from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey, Boolean, String, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class LeaveType(str, enum.Enum):
    """休暇タイプ"""
    PREFERRED_OFF = "preferred_off"  # 希望休
    PAID_LEAVE = "paid_leave"  # 有給
    SUMMER_LEAVE = "summer_leave"  # 夏季休暇
    WINTER_LEAVE = "winter_leave"  # 冬季休暇
    BIRTHDAY_LEAVE = "birthday_leave"  # バースデー休暇


class LeaveRequestStatus(str, enum.Enum):
    """休暇申請ステータス"""
    PENDING = "pending"  # 承認待ち
    APPROVED = "approved"  # 承認済み
    REJECTED = "rejected"  # 却下
    CANCELLED = "cancelled"  # キャンセル


class LeaveRequest(Base):
    """休暇申請モデル"""
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    leave_type = Column(SQLEnum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # ステータス
    status = Column(SQLEnum(LeaveRequestStatus), default=LeaveRequestStatus.PENDING)

    # 理由・メモ
    reason = Column(Text)
    notes = Column(Text)

    # 承認者情報
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション
    employee = relationship("Employee", back_populates="leave_requests")
