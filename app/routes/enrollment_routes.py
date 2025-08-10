from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import EnrollmentCreate, EnrollmentResponse
from app.controllers.enrollment_controller import EnrollmentController
from app.auth import admin_required, teacher_required

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment_data: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Assign a student to a teacher (Admin only)"""
    return EnrollmentController.create_enrollment(enrollment_data, db, background_tasks)

@router.get("/", response_model=List[EnrollmentResponse])
def get_enrollments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(teacher_required)
):
    """Get all enrollments"""
    return EnrollmentController.get_enrollments(db, skip, limit)

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(teacher_required)
):
    """Get enrollment by ID"""
    return EnrollmentController.get_enrollment(enrollment_id, db)

@router.delete("/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """Delete enrollment (Admin only)"""
    return EnrollmentController.delete_enrollment(enrollment_id, db)