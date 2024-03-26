#structure of data in db.
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean,  DateTime
from sqlalchemy import Column
from sqlalchemy import func
from db.base import Base

class DbUser(Base): #inherit from Base in database.py
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True) #id will be primary key for table, automatically create id when insert user some id in db.
    username= Column(String) #we accept str
    email= Column(String)
    password= Column(String) #nobody access the password even in db.
    items= relationship('DbPost', back_populates= 'user')
 
class DbPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    image_url_type = Column(String)
    title = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))  # Corrected the ForeignKey name
    username= Column(String)
    user= relationship('DbUser', back_populates= 'items')
    comments = relationship('DbComment', back_populates= 'post')

class DbComment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('DbPost', back_populates= 'comments')