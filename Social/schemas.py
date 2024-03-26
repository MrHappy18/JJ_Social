from typing import List
from pydantic import BaseModel, EmailStr, ValidationError, validator  #data validation = pydantic = class
import re
from datetime import datetime

#Article inside UserDisplay
class Post(BaseModel):
    title: str
    content: str
    published: bool
    class Config():
        from_attributes = True #orm_mode is changed to from_attributes

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[^\w\s]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Post] = []  #tpye of data which we want return
    class Config():
        from_attributes = True

#user inside article display
class User(BaseModel):
    id:int
    username: str
    class Config():
        from_attributes = True

class PostBase(BaseModel): #what we recieve from the user when we are creating article
    title: str
    content: str
    image_url: str
    image_url_type: str
    creator_id : int
    username: str
    timestamp: datetime

#For Post Display
class CommentBase(BaseModel):
    txt: str
    username: str
    timestamp: datetime
    class Config(): #convert instances of ORM models(db models) into dictionaries whrn serializing the data.
        from_attributes = True

class  PostDisplay(BaseModel): #a data structure to send to the user when we are creating article
    title: str
    content: str
    image_url: str
    image_url_type: str
    user: User
    comments: List[CommentBase]
    timestamp: datetime
    class Config(): #convert instances of ORM models(db models) into dictionaries whrn serializing the data.
        from_attributes = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class CommentBase(BaseModel):
    username: str
    txt: str
    post_id: int
