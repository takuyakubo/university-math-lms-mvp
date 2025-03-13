import os
import sys
from typing import Any, Dict, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.base import Base
from app.main import app
from app.db.base import get_db
from app.models.user import User
from app.models.problem import Problem, Choice, Tag, ProblemTag
from app.models.user_progress import UserAnswer, UserProgress

from .utils import create_test_user, authentication_token_from_user


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """Create a fresh database for each test."""
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Get a test database session
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Close session and roll back the transaction after test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db: Any) -> Generator:
    """Create a test client with an override for the dependency."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    
    # Reset the override after test
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def normal_user(db: Session) -> User:
    """Create a test student user."""
    return create_test_user(
        db=db,
        email="student@example.com",
        password="password123",
        first_name="Test",
        last_name="Student",
        role="student",
    )


@pytest.fixture(scope="function")
def teacher_user(db: Session) -> User:
    """Create a test teacher user."""
    return create_test_user(
        db=db,
        email="teacher@example.com",
        password="password123",
        first_name="Test",
        last_name="Teacher",
        role="teacher",
    )


@pytest.fixture(scope="function")
def student_token_headers(normal_user: User) -> Dict[str, str]:
    """Return authorization headers for student user."""
    return authentication_token_from_user(normal_user)


@pytest.fixture(scope="function")
def teacher_token_headers(teacher_user: User) -> Dict[str, str]:
    """Return authorization headers for teacher user."""
    return authentication_token_from_user(teacher_user)


@pytest.fixture(scope="function")
def test_problem(db: Session, teacher_user: User) -> Problem:
    """Create a test problem with choices."""
    problem = Problem(
        title="Test Problem",
        description="Test description",
        problem_text="Test problem text with math: \\int x dx",
        difficulty=3,
        created_by=teacher_user.id,
    )
    db.add(problem)
    db.flush()
    
    # Add choices
    correct_choice = Choice(
        problem_id=problem.id,
        text="\\frac{x^2}{2} + C",
        is_correct=True,
    )
    wrong_choice = Choice(
        problem_id=problem.id,
        text="x^2 + C",
        is_correct=False,
    )
    db.add(correct_choice)
    db.add(wrong_choice)
    
    # Add tags
    tag = Tag(
        name="calculus",
        description="Calculus problems",
        created_by=teacher_user.id,
    )
    db.add(tag)
    db.flush()
    
    problem_tag = ProblemTag(
        problem_id=problem.id,
        tag_id=tag.id,
    )
    db.add(problem_tag)
    
    db.commit()
    db.refresh(problem)
    return problem