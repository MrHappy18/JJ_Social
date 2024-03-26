from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .hash import Hash  # Make sure this path is correct
from schemas import UserBase  # Make sure this path is correct
from db.models import DbUser
from sqlalchemy.exc import IntegrityError
from .db_user import create_user

SQLALCHEMY_DATABASE_URL = 'sqlite:///./socialwe.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():  # Get a db session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_admin():
    db = SessionLocal()
    try:
        admin_exists = db.query(DbUser).filter(DbUser.username == "admin").first() is not None
        if not admin_exists:
            hashed_password = Hash.bcrypt("admin")  # Hash the admin password
            admin_user = DbUser(username="admin", email="Admin@example.com", password=hashed_password)
            db.add(admin_user)
            db.commit()
        
        # Define and insert other dummy users if needed
        dummy_users = [
            UserBase(username="Alex", email="Alex@example.com", password="Alex!234"),
            UserBase(username="Ben", email="Benn!234@example.com", password="Benn!234"),
        ]

        for user_data in dummy_users:
            try:
                create_user(db=db, request=user_data)
            except IntegrityError:
                db.rollback()  # Handle duplicate entries by rolling back the transaction
    finally:
        db.close()
