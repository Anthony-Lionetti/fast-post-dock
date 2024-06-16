from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import SessionLocal
from ..models import Users
from passlib.context import CryptContext
from typing import Annotated
from datetime import timedelta, datetime, UTC
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

crypt_context = CryptContext(schemes=['sha256_crypt'])

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()

    # Verify username
    if not user:
        return False
    # Verify password
    if not crypt_context.verify(password, user.hashed_password):
        return False
    
    return user

# Hardcode SECRET_KEY & ALGORITHM for now
SECRET_KEY = 'ca516fa563535cf6ca745d406b4a19e4358230a8749215aa3aea5ae30bad60b1'
ALGORITHM = 'HS256'

def create_access_token(username:str, user_id:str, role:str, expires_delta:timedelta):
    encode = {'sub': username, 'id':user_id, 'role':role}
    expires = datetime.now(UTC) + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

class Token(BaseModel):
    access_token:str
    token_type:str

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str 


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password = crypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}