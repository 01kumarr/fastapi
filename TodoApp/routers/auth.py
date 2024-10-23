from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone


router = APIRouter(
    prefix="/auth",
    tags=['auth']
) 

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = 'c62368e9e1c2ecb1b76ab2d30d262c5959d43bc2a44e51d4bd118566efee3f6'
ALGORITHM = 'HS256'



# method to get db
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False 

    if not bcrypt_context.verify(password, user.hashed_password):
        return False 
    return user 


def create_access_token(username:str, user_id:int, role:str, expires_delta:timedelta):

    encode = {'sub':username, 'id': user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta 
    encode.update({'exp': expires}) 

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) 
        username :str = payload.get('sub') 
        user_id :int = payload.get('id')
        user_role:str = payload.get('role')  
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user") 
        return {'username':username, 'id':user_id, 'role':user_role} 
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user")


## get db dependancy
db_dependancy = Annotated[ Session, Depends(get_db)] 


# pydantic class to take user request to create user
class CreateUserRequest(BaseModel):
    username : str
    email : str 
    first_name : str 
    last_name : str 
    password : str 
    role : str 

class Token(BaseModel):
    access_token :str
    token_type:str 

@router.get("/", status_code=status.HTTP_200_OK)
async def read_db(db: db_dependancy):
    return db.query(Users).all()

## hasing password before adding them into database...
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependancy, create_user_request : CreateUserRequest):
    try:
        exsiting_user = db.query(Users).filter(Users.username == create_user_request.username)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists") 
    
    except NoResultFound:
        create_user_model = Users(
            email = create_user_request.email,
            username = create_user_request.username,
            first_name = create_user_request.first_name,
            last_name = create_user_request.last_name,
            role = create_user_request.role,
            hashed_password = bcrypt_context.hash(create_user_request.password),
            is_active = True 
        )

        db.add(create_user_model)
        db.commit() 


### User authentication. using token JWT
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
                                db : db_dependancy):
    user = authenticate_user(form_data.username, form_data.password, db) 

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user")  

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token':token, 'token_type':'bearer'}
