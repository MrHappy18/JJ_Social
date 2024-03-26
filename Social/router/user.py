from typing import List
from schemas import UserBase,UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user, oauth2_scheme


router = APIRouter(
    prefix= '/user',
    tags=['user']
)

#Create User
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

#Read All Users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session= Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db_user.get_all_user(db)

#Read a user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db:Session =  Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db_user.get_user(db, id)

#Update User
@router.post('/{id}/update')
def update_user(id: int, request:UserBase, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db_user.update_user(db, id, request)

#Delete User
@router.get('/{id}/delete')
def delete_user(id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db_user.delete_user(db, id)
