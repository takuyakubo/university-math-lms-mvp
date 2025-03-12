"""
Database seeding script for the Math LMS application.
This script creates sample data in the database for development and testing.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import app modules
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal

# Import models
# from app.models.user import User
# Import other models as needed


def seed_users(db: Session) -> None:
    """Seed sample users into the database."""
    # Example:
    # users = [
    #    User(
    #        email="admin@example.com",
    #        hashed_password="hashed_password_here",  # Use actual hashing in real app
    #        is_active=True,
    #        is_superuser=True,
    #        full_name="Admin User"
    #    ),
    #    User(
    #        email="student@example.com",
    #        hashed_password="hashed_password_here",  # Use actual hashing in real app
    #        is_active=True,
    #        full_name="Student User"
    #    ),
    # ]
    # for user in users:
    #    db.add(user)
    
    print("Users seeded successfully")


def seed_courses(db: Session) -> None:
    """Seed sample courses into the database."""
    # Example:
    # courses = [
    #    Course(
    #        title="Calculus I",
    #        description="Introduction to differential calculus",
    #        level="undergraduate",
    #    ),
    # ]
    # for course in courses:
    #    db.add(course)
    
    print("Courses seeded successfully")


def main() -> None:
    """Main function to run the database seeding."""
    db = SessionLocal()
    try:
        # Uncomment these as models are implemented
        # seed_users(db)
        # seed_courses(db)
        
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()