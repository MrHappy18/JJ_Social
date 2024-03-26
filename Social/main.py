from fastapi import FastAPI
from router import user, userwall, comment
from db import models
from db.database import engine, insert_admin
from sqlalchemy.orm import Session
from auth import authentication
from fastapi.staticfiles import StaticFiles
from os import name
from auth import authentication



app=FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(userwall.router)
app.include_router(comment.router)


@app.get('/')
def index():
    return {'Hello! Welcome to NakamaNet'}

@app.on_event("startup")
def startup_event():
    insert_admin()


models.Base.metadata.create_all(engine)  #db engine

app.mount('/images', StaticFiles(directory='images'), name='images')