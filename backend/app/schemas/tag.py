from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None


class TagCreate(TagBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "微分積分学",
                "description": "微分積分学に関連する問題"
            }
        }


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "微分積分学（Calculus）に関連する問題"
            }
        }


class TagResponse(TagBase):
    id: UUID
    created_by: UUID
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "微分積分学",
                "description": "微分積分学に関連する問題",
                "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa7"
            }
        }