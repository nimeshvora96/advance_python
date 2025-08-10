from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from app.models import Enrollment, Student, Teacher
from app.schemas import EnrollmentCreate
from app.controllers.student_controller import StudentController
from app.controllers.teacher_controller import TeacherController
from app.utils.background_tasks import send_enrollment_email
from app.utils.cache import cache

class EnrollmentController:
    @staticmethod
    def create_enrollment(
        enrollment_data: EnrollmentCreate,
        db: Session,
        background_tasks: BackgroundTasks
    ):
        # Verify student and teacher exist
        student = StudentController.get_student(enrollment_data.student_id, db)
        teacher = TeacherController.get_teacher(enrollment_data.teacher_id, db)
        
        # Check if enrollment already exists
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == enrollment_data.student_id,
            Enrollment.teacher_id == enrollment_data.teacher_id
        ).first()
        
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is already enrolled with this teacher"
            )
        
        # Create enrollment
        db_enrollment = Enrollment(**enrollment_data.dict())
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        
        # Invalidate students cache since enrollment affects student data
        cache.invalidate_pattern("students:*")
        
        # Trigger background task for email notification
        background_tasks.add_task(
            send_enrollment_email,
            student.email,
            teacher.name,
            student.name
        )
        
        return db_enrollment
    
    @staticmethod
    def get_enrollments(db: Session, skip: int = 0, limit: int = 100):
        enrollments = db.query(Enrollment).offset(skip).limit(limit).all()
        return enrollments
    
    @staticmethod
    def get_enrollment(enrollment_id: int, db: Session):
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        return enrollment
    
    @staticmethod
    def delete_enrollment(enrollment_id: int, db: Session):
        enrollment = EnrollmentController.get_enrollment(enrollment_id, db)
        db.delete(enrollment)
        db.commit()
        
        # Invalidate cache
        cache.invalidate_pattern("students:*")
        
        return {"message": "Enrollment deleted successfully"}