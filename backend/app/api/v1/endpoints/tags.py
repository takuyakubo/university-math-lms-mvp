from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.problem import Tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.auth import get_current_active_user, get_current_teacher

router = APIRouter()


@router.get("", response_model=List[TagResponse])
def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    タグ一覧を取得する
    """
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    新しいタグを作成する (教員のみ)
    """
    # 既存のタグがあるか確認
    tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
    if tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The tag with this name already exists",
        )
    
    # 新しいタグを作成
    tag = Tag(
        name=tag_in.name,
        description=tag_in.description,
        created_by=current_user.id,
    )
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("/{tag_id}", response_model=TagResponse)
def read_tag(
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    タグの詳細情報を取得する
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: str,
    tag_in: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    タグを更新する (教員のみ)
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    
    # 同名の別タグがあるか確認
    if tag_in.name and tag_in.name != tag.name:
        existing_tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The tag with this name already exists",
            )
    
    # タグの更新
    update_data = tag_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
    
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> None:
    """
    タグを削除する (教員のみ)
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    
    db.delete(tag)
    db.commit()