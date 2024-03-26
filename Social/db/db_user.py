from db.hash import Hash
from sqlalchemy.orm.session import Session 
from schemas import UserBase
from db.models import DbUser
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db.hash import Hash

def create_user(db: Session, request: UserBase):
    hashed_password = Hash.bcrypt(request.password)  # Ensure Hash.bcrypt is the correct method call for hashing
    new_user = DbUser(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_user(db: Session):
    return db.query(DbUser).all()

def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found') 
    return user

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)  # Ensure password is hashed
    db.commit()
    return 'ok'

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    db.delete(user)
    db.commit()
    return 'ok'