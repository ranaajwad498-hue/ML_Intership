import jwt
from database import session_local
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from model import User


def getdb():
    db= session_local()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "ajwad321"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash= PasswordHash((BcryptHasher(),))
oauth_scheme= OAuth2PasswordBearer(tokenUrl="/login")

class authentication():
    
    def hash_password(password:str):
        return password_hash.hashers(password)

    def verify_password(plain_password:str, hashed_passsword:str)->bool:
        return password_hash.verify(plain_password, hashed_passsword)


    def create_access_token(data:dict, expires_delta:Optional[timedelta]=None)->str:
        to_encode= data.copy()
        if expires_delta:
            expire= datetime.now(timezone.utc) + expires_delta
        else:
            expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp":expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(token:str=Depends(oauth_scheme), db:Session= Depends(getdb))->User:
        credentials_expection= HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail=" Could not Validates Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

        try:
            payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise credentials_expection

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOken has Expired",
            )

        except jwt.PyJWTError:
            raise credentials_expection

        user= db.query(User).filter(User.u_id == user_id).first()
        if user is None:
            raise credentials_expection

        return user
