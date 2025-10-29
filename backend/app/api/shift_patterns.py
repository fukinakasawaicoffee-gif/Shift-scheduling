from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.shift_pattern import ShiftPattern
from app.schemas.shift_pattern import (
    ShiftPattern as ShiftPatternSchema,
    ShiftPatternCreate,
    ShiftPatternUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[ShiftPatternSchema])
def get_shift_patterns(
    department_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフトパターン一覧取得"""
    query = db.query(ShiftPattern)

    if department_id:
        query = query.filter(ShiftPattern.department_id == department_id)

    patterns = query.offset(skip).limit(limit).all()
    return patterns


@router.get("/{pattern_id}", response_model=ShiftPatternSchema)
def get_shift_pattern(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフトパターン詳細取得"""
    pattern = db.query(ShiftPattern).filter(ShiftPattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="シフトパターンが見つかりません")
    return pattern


@router.post("/", response_model=ShiftPatternSchema)
def create_shift_pattern(
    pattern_in: ShiftPatternCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフトパターン作成"""
    pattern = ShiftPattern(**pattern_in.dict())
    db.add(pattern)
    db.commit()
    db.refresh(pattern)
    return pattern


@router.put("/{pattern_id}", response_model=ShiftPatternSchema)
def update_shift_pattern(
    pattern_id: int,
    pattern_in: ShiftPatternUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフトパターン更新"""
    pattern = db.query(ShiftPattern).filter(ShiftPattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="シフトパターンが見つかりません")

    update_data = pattern_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pattern, field, value)

    db.commit()
    db.refresh(pattern)
    return pattern


@router.delete("/{pattern_id}")
def delete_shift_pattern(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """シフトパターン削除"""
    pattern = db.query(ShiftPattern).filter(ShiftPattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="シフトパターンが見つかりません")

    db.delete(pattern)
    db.commit()
    return {"message": "削除しました"}
