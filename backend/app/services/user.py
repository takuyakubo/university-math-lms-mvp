from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import get_password_hash


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_create: UserCreate) -> User:
    db_user = User(
        email=user_create.email,
        password_hash=get_password_hash(user_create.password),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        role=user_create.role,
        is_active=True,
        is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    update_data = user_update.dict(exclude_unset=True)
    
    if update_data.get("password"):
        update_data["password_hash"] = get_password_hash(update_data["password"])
        del update_data["password"]
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> bool:
    db.delete(user)
    db.commit()
    return True