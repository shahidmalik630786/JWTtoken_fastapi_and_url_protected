from fastapi import APIRouter,HTTPException,status
from schemas import UserSchema,Token,CustomOAuth2PasswordRequestForm,TokenData
from sqlalchemy.orm import Session
from dependencies import get_db
from fastapi import Depends
from operations import register_user,get_all_user
from typing import List
from token_util import create_access_token,create_refresh_token,JWT_SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_MINUTES,ALGORITHM,decode_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models import User
from hashing import verify_password
from jose import jwt, JWTError


router = APIRouter(tags=['Authentication'])


@router.post('/login',response_model=Token)
async def login(form_data: CustomOAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(user.email, expires_delta=refresh_token_expires)
    print(access_token,"access token***********")
    print(refresh_token,"refresh token***********")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post('/register',response_model=UserSchema)
def register(username:str,email:str,password:str,db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    db_user = register_user(db,username,email,password)
    return db_user



@router.get("/alluser/")
def read_users(token_data: TokenData = Depends(decode_token),db: Session = Depends(get_db)):
    return {"message": "This is a protected route", "data": get_all_user(db)}



@router.get("/protected_route")
async def protected_route(token_data: TokenData = Depends(decode_token)):
    return {"message": "This is a protected route", "username": token_data.username}