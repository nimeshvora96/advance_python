from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import StudentCreate, StudentUpdate, StudentResponse, TeacherResponse
from app.controllers.student_controller import StudentController
from app.auth import admin_required, teacher_required
from fastapi import Body
from typing import Optional


router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Create a new student (Admin only)"""
    return StudentController.create_student(student_data, db)

@router.get("/", response_model=List[dict])
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(teacher_required)
):
    """Get all students with caching (Teacher/Admin access)"""
    return StudentController.get_students(db, skip, limit)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(teacher_required)
):
    """Get student by ID"""
    return StudentController.get_student(student_id, db)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: Optional[StudentUpdate] = Body(None),
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Update student (Admin only)"""
    return StudentController.update_student(student_id, student_data, db)

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Delete student (Admin only)"""
    return StudentController.delete_student(student_id, db)

