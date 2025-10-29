from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.shift_requirement import ShiftRequirement
from app.schemas.shift_requirement import (
    ShiftRequirement as ShiftRequirementSchema,
    ShiftRequirementCreate,
    ShiftRequirementUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[ShiftRequirementSchema])
def get_shift_requirements(
    department_id: int = None,
    start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフト必要人数一覧取得"""
    query = db.query(ShiftRequirement)

    if department_id:
        query = query.filter(ShiftRequirement.department_id == department_id)

    if start_date:
        query = query.filter(ShiftRequirement.date >= start_date)

    if end_date:
        query = query.filter(ShiftRequirement.date <= end_date)

    requirements = query.offset(skip).limit(limit).all()
    return requirements


@router.get("/{requirement_id}", response_model=ShiftRequirementSchema)
def get_shift_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフト必要人数詳細取得"""
    requirement = db.query(ShiftRequirement).filter(ShiftRequirement.id == requirement_id).first()
    if not requirement:
        raise HTTPException(status_code=404, detail="シフト必要人数が見つかりません")
    return requirement


@router.post("/", response_model=ShiftRequirementSchema)
def create_shift_requirement(
    requirement_in: ShiftRequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフト必要人数作成"""
    requirement = ShiftRequirement(**requirement_in.dict())
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return requirement


@router.put("/{requirement_id}", response_model=ShiftRequirementSchema)
def update_shift_requirement(
    requirement_id: int,
    requirement_in: ShiftRequirementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフト必要人数更新"""
    requirement = db.query(ShiftRequirement).filter(ShiftRequirement.id == requirement_id).first()
    if not requirement:
        raise HTTPException(status_code=404, detail="シフト必要人数が見つかりません")

    update_data = requirement_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(requirement, field, value)

    db.commit()
    db.refresh(requirement)
    return requirement


@router.delete("/{requirement_id}")
def delete_shift_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフト必要人数削除"""
    requirement = db.query(ShiftRequirement).filter(ShiftRequirement.id == requirement_id).first()
    if not requirement:
        raise HTTPException(status_code=404, detail="シフト必要人数が見つかりません")

    db.delete(requirement)
    db.commit()
    return {"message": "削除しました"}
