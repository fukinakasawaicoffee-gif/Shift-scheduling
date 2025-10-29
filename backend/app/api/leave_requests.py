from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.leave_request import LeaveRequest, LeaveRequestStatus
from app.schemas.leave_request import (
    LeaveRequest as LeaveRequestSchema,
    LeaveRequestCreate,
    LeaveRequestUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[LeaveRequestSchema])
def get_leave_requests(
    employee_id: int = None,
    status: LeaveRequestStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請一覧取得"""
    query = db.query(LeaveRequest)

    if employee_id:
        query = query.filter(LeaveRequest.employee_id == employee_id)

    if status:
        query = query.filter(LeaveRequest.status == status)

    requests = query.offset(skip).limit(limit).all()
    return requests


@router.get("/{request_id}", response_model=LeaveRequestSchema)
def get_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請詳細取得"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="休暇申請が見つかりません")
    return leave_request


@router.post("/", response_model=LeaveRequestSchema)
def create_leave_request(
    request_in: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請作成"""
    leave_request = LeaveRequest(**request_in.dict())
    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.put("/{request_id}", response_model=LeaveRequestSchema)
def update_leave_request(
    request_id: int,
    request_in: LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請更新"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="休暇申請が見つかりません")

    update_data = request_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(leave_request, field, value)

    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.post("/{request_id}/approve", response_model=LeaveRequestSchema)
def approve_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請を承認"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="休暇申請が見つかりません")

    leave_request.status = LeaveRequestStatus.APPROVED
    leave_request.approved_by = current_user.id
    leave_request.approved_at = datetime.utcnow()

    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.post("/{request_id}/reject", response_model=LeaveRequestSchema)
def reject_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請を却下"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="休暇申請が見つかりません")

    leave_request.status = LeaveRequestStatus.REJECTED
    leave_request.approved_by = current_user.id
    leave_request.approved_at = datetime.utcnow()

    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.delete("/{request_id}")
def delete_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """休暇申請削除"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="休暇申請が見つかりません")

    db.delete(leave_request)
    db.commit()
    return {"message": "削除しました"}
