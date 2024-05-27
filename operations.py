from sqlalchemy.orm import Session
from models import User
from hashing import hashed_password,verify_password


def login_credentials(db:Session,username:str, password:str):
        db_user = db.query(User).filter(User.username == username).first()
        if db_user and verify_password(password, db_user.password):  
            return db_user
        return None
    
def register_user(db:Session,username:str, email:str,password:str):
    hash_password = hashed_password(password)
    db_user=User(username = username,email=email,password = hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_user(db:Session):
    return db.query(User).all()