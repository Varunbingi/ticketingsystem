from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from db.models.user import User
from pwdlib import PasswordHash
from datetime import timedelta, datetime
from jose import jwt, JWTError
from utils.settings import config
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy import select

password_hash = PasswordHash.recommended()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def authenticate_user(
        username: str,
        password: str,
        db: AsyncSession = Depends(get_async_session)
        ):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="Not authorized user or user not found in the system")
    if not password_hash.verify(password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect password")
    return user

def create_user_token(
        username: str, user_id: str, expires_delta: timedelta
        ):
    encode = {'sub': username, 'id': str(user_id)}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires}) 
    return jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms= config.ALGORITHM)
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")
        return {"username": username, "id": int(user_id)}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")