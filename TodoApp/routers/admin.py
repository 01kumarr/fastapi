from typing import Annotated
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends, HTTPException
from models import Todos, Users
from database import SessionLocal
from starlette import status
from pydantic import BaseModel 
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['auth']
) 


## create a function to get database 
def get_db():
    db = SessionLocal() 
    try:
        yield db 
    finally:
        db.close() 

db_dependency = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependancy, db:db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all() 
