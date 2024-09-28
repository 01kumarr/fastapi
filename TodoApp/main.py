from fastapi import FastAPI 
import models 
from database import engine 

app = FastAPI() 

# create a table in the database todos
models.Base.metadata.create_all(bind=engine) 
