from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.department import Department
from app.schemas.department import Department as DepartmentSchema, DepartmentCreate, DepartmentUpdate

router = APIRouter()


@router.get("/", response_model=List[DepartmentSchema])
def get_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """部署一覧取得"""
    departments = db.query(Department).offset(skip).limit(limit).all()
    return departments


@router.get("/{department_id}", response_model=DepartmentSchema)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """部署詳細取得"""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="部署が見つかりません")
    return department


@router.post("/", response_model=DepartmentSchema)
def create_department(
    department_in: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """部署作成"""
    department = Department(**department_in.dict())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.put("/{department_id}", response_model=DepartmentSchema)
def update_department(
    department_id: int,
    department_in: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """部署更新"""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="部署が見つかりません")

    update_data = department_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(department, field, value)

    db.commit()
    db.refresh(department)
    return department


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """部署削除"""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="部署が見つかりません")

    db.delete(department)
    db.commit()
    return {"message": "削除しました"}
