from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class UserAnswerBase(BaseModel):
    problem_id: UUID
    selected_choice: UUID


class UserAnswerCreate(UserAnswerBase):
    class Config:
        json_schema_extra = {
            "example": {
                "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "selected_choice": "3fa85f64-5717-4562-b3fc-2c963f66afa7"
            }
        }


class UserAnswerResponse(UserAnswerBase):
    id: UUID
    user_id: UUID
    is_correct: bool
    created_at: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                "selected_choice": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "is_correct": True,
                "created_at": "2023-01-01T00:00:00"
            }
        }


class UserProgressResponse(BaseModel):
    user_id: UUID
    problem_id: UUID
    attempts: int
    last_attempt_at: Optional[str] = None
    mastery_level: float
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "attempts": 3,
                "last_attempt_at": "2023-01-01T00:00:00",
                "mastery_level": 0.8
            }
        }