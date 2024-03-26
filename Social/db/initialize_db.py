# initialize_db.py
from sqlalchemy.orm import Session
from db.session import SessionLocal  # Adjust based on your actual session factory
from db.db_user import create_user
from schemas import UserBase

def insert_dummy_users(db: Session):
    # Check if we already have users in the database
    if db.query(DbUser).first() is not None:
        return  # Skip if users already exist

    # Define dummy users
    dummy_users = [
        UserBase(username="Admin", email="Admin@example.com", password="Admin"),
        UserBase(username="Alex", email="Alex@example.com", password="Alex!234"),
        UserBase(username="Ben", email="Benn!234@example.com", password="Benn!234"),
    ]

    # Insert dummy users into the database
    for user in dummy_users:
        create_user(db, user)

def main():
    db = SessionLocal()
    insert_dummy_users(db)
    db.close()

if __name__ == "__main__":
    main()
