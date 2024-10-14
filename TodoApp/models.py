## This file is used to create schema of database

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

## User class 
class Users(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True) 
    username = Column(String, unique=True) 
    first_name = Column(String) 
    last_name = Column(String) 
    hashed_password = Column(String) 
    is_active = Column(Boolean, default=True) 
    role = Column(String)

## creating a model class by inheriting base class from declarative_base..
class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String)
    description = Column(String) 
    priority = Column(String)
    complete = Column(Boolean) 
    owner_id = Column(Integer, ForeignKey("users.id"))
