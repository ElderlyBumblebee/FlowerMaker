from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from src.auth.security import decode_access_token
from src.core.database import get_db
from src.core.models import User


def get_current_user_optional(
    request: Request, db: Session = Depends(get_db)
) -> User | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    user_id = decode_access_token(token)
    if user_id is None:
        return None
    return db.get(User, user_id)


def get_current_user(user: User | None = Depends(get_current_user_optional)) -> User:
    if user is None:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user