from database import Base
from sqlalchemy import Column, Integer, String, Boolean


## creating a model class by inheriting base class from declarative_base..
class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True) 
    titel = Column(String)
    description = Column(String) 
    priority = Column(String) 
    complete = Column(String) 
