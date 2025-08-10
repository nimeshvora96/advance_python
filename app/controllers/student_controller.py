from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Student, Teacher, Enrollment
from app.schemas import StudentCreate, StudentUpdate
from app.utils.cache import cache
from typing import List

class StudentController:
    @staticmethod
    def create_student(student_data: StudentCreate, db: Session):
        # Check if email exists
        existing_student = db.query(Student).filter(Student.email == student_data.email).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this email already exists"
            )
        
        db_student = Student(**student_data.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        # Invalidate cache
        cache.invalidate_pattern("students:*")
        
        return db_student
    
    @staticmethod
    def get_students(db: Session, skip: int = 0, limit: int = 100):
        cache_key = f"students:list:{skip}:{limit}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        students = db.query(Student).offset(skip).limit(limit).all()
        students_data = [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "phone": s.phone,
                "course": s.course,
                "created_at": s.created_at
            } for s in students
        ]
        
        # Cache for 30 seconds
        cache.set(cache_key, students_data, expire=30)
        
        return students_data
    
    @staticmethod
    def get_student(student_id: int, db: Session):
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return student
    
    @staticmethod
    def update_student(student_id: int, student_data: StudentUpdate, db: Session):
        student = StudentController.get_student(student_id, db)

        if student_data is None:
            return student
        
        for field, value in student_data.dict(exclude_unset=True).items():
            setattr(student, field, value)
        
        db.commit()
        db.refresh(student)
        
        # Invalidate cache
        cache.invalidate_pattern("students:*")
        
        return student
    
    @staticmethod
    def delete_student(student_id: int, db: Session):
        student = StudentController.get_student(student_id, db)
        db.delete(student)
        db.commit()
        
        # Invalidate cache
        cache.invalidate_pattern("students:*")
        
        return {"message": "Student deleted successfully"}
    
    