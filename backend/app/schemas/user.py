from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field("student", pattern="^(student|teacher)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "first_name": "太郎",
                "last_name": "山田",
                "role": "student",
                "password": "securepassword"
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "太郎",
                "last_name": "山田",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword"
            }
        }


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "email": "user@example.com",
                "first_name": "太郎",
                "last_name": "山田",
                "role": "student",
                "is_active": True,
                "is_verified": True,
                "created_at": "2023-01-01T00:00:00",
            }
        }