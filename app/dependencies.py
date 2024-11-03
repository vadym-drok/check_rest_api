from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
import jwt
from app.crud import get_user_by_username
from fastapi import HTTPException
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
