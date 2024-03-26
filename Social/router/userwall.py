from auth.oauth2 import get_current_user
from schemas import PostBase, PostDisplay, UserAuth
from fastapi import APIRouter, Depends, UploadFile, status, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_post
from fileinput import filename
from auth.oauth2 import oauth2_scheme
from os import path
from typing import List
import random
import string
import shutil
import os


router = APIRouter(
    prefix= '/userwall',
    tags=['userwall']
)

#This is used to post image to user DB images
@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    letters = string.ascii_letters  
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filepath': path}

image_url_types = ['absolute', 'relative']

@router.post('', response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take values ‘absolute’ or 'relative'.")
    return db_post.create_post(db, request)

# Get all posts from User 
@router.get('/all', response_model=List[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)

#get spesific post
@router.get('/{id}') #, response_model=PostDisplay)
def get_post(id:int, db:Session = Depends(get_db)): #secure end-point #token: str = Depends(oauth2_scheme)
    return {
        'data': db_post.get_post(db,id)
    }

#Update User
@router.post('/{id}/update')
def update_post(id: int, request:PostBase, db:Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db_post.update_post(db, id, request)

#Delete Post
@router.get('/delete/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db_post.delete_post(db, id, current_user.id)




