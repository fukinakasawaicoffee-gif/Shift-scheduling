from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.schedule import Schedule
from app.schemas.schedule import (
    Schedule as ScheduleSchema,
    ScheduleCreate,
    ScheduleUpdate,
    GenerateScheduleRequest,
    GenerateScheduleResponse,
)
from app.services.schedule_service import ScheduleService

router = APIRouter()


@router.post("/generate", response_model=GenerateScheduleResponse)
def generate_schedule(
    request: GenerateScheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフト自動生成"""
    service = ScheduleService(db)
    result = service.generate_schedule(
        department_id=request.department_id,
        start_date=request.start_date,
        end_date=request.end_date,
        time_limit_seconds=request.time_limit_seconds,
    )

    return GenerateScheduleResponse(**result)


@router.get("/", response_model=List[ScheduleSchema])
def get_schedules(
    department_id: int = None,
    employee_id: int = None,
    start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """スケジュール一覧取得"""
    query = db.query(Schedule)

    if department_id:
        from app.models.employee import Employee
        query = query.join(Employee).filter(Employee.department_id == department_id)

    if employee_id:
        query = query.filter(Schedule.employee_id == employee_id)

    if start_date:
        query = query.filter(Schedule.date >= start_date)

    if end_date:
        query = query.filter(Schedule.date <= end_date)

    schedules = query.offset(skip).limit(limit).all()
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleSchema)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """スケジュール詳細取得"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="スケジュールが見つかりません")
    return schedule


@router.post("/", response_model=ScheduleSchema)
def create_schedule(
    schedule_in: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """スケジュール作成"""
    schedule = Schedule(**schedule_in.dict())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleSchema)
def update_schedule(
    schedule_id: int,
    schedule_in: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """スケジュール更新"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="スケジュールが見つかりません")

    update_data = schedule_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(schedule, field, value)

    db.commit()
    db.refresh(schedule)
    return schedule


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """スケジュール削除"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="スケジュールが見つかりません")

    db.delete(schedule)
    db.commit()
    return {"message": "削除しました"}
