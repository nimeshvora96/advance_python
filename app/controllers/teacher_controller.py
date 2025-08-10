from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Teacher, Student, Enrollment
from app.schemas import TeacherCreate, TeacherUpdate

class TeacherController:
    @staticmethod
    def create_teacher(teacher_data: TeacherCreate, db: Session):
        db_teacher = Teacher(**teacher_data.dict())
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    
    @staticmethod
    def get_teachers(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Teacher).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_teacher(teacher_id: int, db: Session):
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )
        return teacher
    
    @staticmethod
    def update_teacher(teacher_id: int, teacher_data: TeacherUpdate, db: Session):
        teacher = TeacherController.get_teacher(teacher_id, db)

        if teacher_data is None:
            return teacher
        
        for field, value in teacher_data.dict(exclude_unset=True).items():
            setattr(teacher, field, value)
        
        db.commit()
        db.refresh(teacher)
        return teacher
    
    @staticmethod
    def delete_teacher(teacher_id: int, db: Session):
        teacher = TeacherController.get_teacher(teacher_id, db)
        db.delete(teacher)
        db.commit()
        return {"message": "Teacher deleted successfully"}
    