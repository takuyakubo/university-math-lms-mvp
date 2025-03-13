from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenPayload(BaseModel):
    sub: str
    exp: int
    role: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "sub": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "exp": 1672531200,  # 2023-01-01 00:00:00 UTC
                "role": "student"
            }
        }