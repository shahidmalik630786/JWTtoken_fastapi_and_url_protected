from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Union,Annotated
from dependencies import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

class UserSchema(BaseModel):
    username:str
    email:str
    password:str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class CustomOAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str

db_dependency = Annotated[Session, Depends(get_db)]