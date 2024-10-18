
from fastapi import FastAPI
import models
from models import Todos
from database import engine
from routers import auth, todos

app = FastAPI() 

# create a table in the database (todos)
models.Base.metadata.create_all(bind=engine) 

app.include_router(auth.router)
app.include_router(todos.router)

