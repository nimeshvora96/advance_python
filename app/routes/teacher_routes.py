from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import TeacherCreate, TeacherUpdate, TeacherResponse, StudentResponse
from app.controllers.teacher_controller import TeacherController
from app.auth import admin_required, teacher_required
from fastapi import Body
from typing import Optional

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Create a new teacher (Admin only)"""
    return TeacherController.create_teacher(teacher_data, db)

@router.get("/", response_model=List[TeacherResponse])
def get_teachers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(teacher_required)
):
    """Get all teachers"""
    return TeacherController.get_teachers(db, skip, limit)

@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(teacher_required)
):
    """Get teacher by ID"""
    return TeacherController.get_teacher(teacher_id, db)

@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: int,
    teacher_data: Optional[TeacherUpdate] = Body(None),
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Update teacher (Admin only)"""
    return TeacherController.update_teacher(teacher_id, teacher_data, db)

@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Delete teacher (Admin only)"""
    return TeacherController.delete_teacher(teacher_id, db)
