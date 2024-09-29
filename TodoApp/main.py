from typing import Annotated
from sqlalchemy.orm import Session 
from fastapi import FastAPI, Depends
import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI() 

# create a table in the database todos
models.Base.metadata.create_all(bind=engine) 


## create a functimn to get database 
def get_db():
    db = SessionLocal() 
    try:
        yield db 
    finally:
        db.close() 

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
async def read_db(db: db_dependency):
    return db.query(Todos).all()


