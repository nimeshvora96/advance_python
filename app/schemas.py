from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    course: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Teacher Schemas
class TeacherBase(BaseModel):
    name: str
    department: str

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None

class TeacherResponse(TeacherBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Enrollment Schemas
class EnrollmentBase(BaseModel):
    student_id: int
    teacher_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_on: datetime
    student: StudentResponse
    teacher: TeacherResponse
    
    class Config:
        from_attributes = True

# Response Schemas with relationships
class StudentWithTeachers(StudentResponse):
    teachers: List[TeacherResponse] = []

class TeacherWithStudents(TeacherResponse):
    students: List[StudentResponse] = []