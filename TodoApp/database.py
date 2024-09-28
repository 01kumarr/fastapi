from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


## database location in sqlite..with name (todos)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' 

# create an engine to communicate with database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) 

#It's responsible for managing all the database operations, like querying the database, 
# adding new records, and committing changes.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

"""
When you're working with SQLAlchemy's ORM, you define models (Python classes that map to database tables). 
These models need to inherit from the base class provided by declarative_base
"""
Base = declarative_base()

