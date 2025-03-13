from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ChoiceBase(BaseModel):
    text: str = Field(..., min_length=1)
    is_correct: bool = False


class ChoiceCreate(ChoiceBase):
    class Config:
        json_schema_extra = {
            "example": {
                "text": "\\frac{x^2}{2} + C",
                "is_correct": True
            }
        }


class ChoiceResponse(ChoiceBase):
    id: UUID
    problem_id: UUID
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "text": "\\frac{x^2}{2} + C",
                "is_correct": True
            }
        }


class ProblemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    problem_text: str = Field(..., min_length=1)
    difficulty: int = Field(3, ge=1, le=5)


class ProblemCreate(ProblemBase):
    choices: List[ChoiceCreate] = Field(..., min_items=2)
    tags: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "積分の基本公式",
                "description": "x^nの不定積分を求める問題",
                "problem_text": "\\int x dx",
                "difficulty": 3,
                "choices": [
                    {
                        "text": "\\frac{x^2}{2} + C",
                        "is_correct": True
                    },
                    {
                        "text": "x^2 + C",
                        "is_correct": False
                    }
                ],
                "tags": ["微分積分学", "不定積分"]
            }
        }


class ProblemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    problem_text: Optional[str] = Field(None, min_length=1)
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "積分の基本公式（修正版）",
                "difficulty": 2
            }
        }


class ProblemResponse(ProblemBase):
    id: UUID
    created_by: UUID
    created_at: str
    choices: List[ChoiceResponse]
    tags: Optional[List[str]] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "積分の基本公式",
                "description": "x^nの不定積分を求める問題",
                "problem_text": "\\int x dx",
                "difficulty": 3,
                "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "created_at": "2023-01-01T00:00:00",
                "choices": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                        "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "text": "\\frac{x^2}{2} + C",
                        "is_correct": True
                    },
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                        "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "text": "x^2 + C",
                        "is_correct": False
                    }
                ],
                "tags": ["微分積分学", "不定積分"]
            }
        }


class ProblemList(BaseModel):
    items: List[ProblemResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "title": "積分の基本公式",
                        "description": "x^nの不定積分を求める問題",
                        "problem_text": "\\int x dx",
                        "difficulty": 3,
                        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                        "created_at": "2023-01-01T00:00:00",
                        "choices": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                                "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "text": "\\frac{x^2}{2} + C",
                                "is_correct": True
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                                "problem_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "text": "x^2 + C",
                                "is_correct": False
                            }
                        ],
                        "tags": ["微分積分学", "不定積分"]
                    }
                ],
                "total": 1
            }
        }