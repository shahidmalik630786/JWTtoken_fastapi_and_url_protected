from sqlalchemy.orm import Session
from fastapi import Depends
from models import SessionLocal
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from token_util import (
    ALGORITHM,
    JWT_SECRET_KEY,
)

from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
#     try:
#         payload = jwt.decode(
#             token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
        
#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             raise HTTPException(
#                 status_code = status.HTTP_401_UNAUTHORIZED,
#                 detail="Token expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except(jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
        
#     user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
    
    
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Could not find user",
#         )
    
#     return SystemUser(**user)
