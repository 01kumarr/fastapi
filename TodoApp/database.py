from sqlalchemy import create_engine

## database location in sqlite..with name (todos)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' 

# create an engine to communicate with database
enigne = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) 

