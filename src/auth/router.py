from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user_optional
from src.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)
from src.core.database import get_db
from src.core.models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def redirect_with_cookie(url: str, user_id: int) -> RedirectResponse:
    response = RedirectResponse(url, status_code=303)
    response.set_cookie(
        key="access_token",
        value=create_access_token(user_id),
        httponly=True,   
        samesite="lax",  
        secure=False,    
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response


@router.get("/register")
def register_page(request: Request, user: User | None = Depends(get_current_user_optional)):
    return templates.TemplateResponse(request, "register.html", {"user": user})


@router.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()
    error = None
    if len(password) < 8:
        error = "Password must be at least 8 characters."
    elif len(password.encode()) > 72:
        error = "Password is too long (max 72 bytes)."
    elif db.scalar(select(User).where(User.email == email)):
        error = "This email is already registered."

    if error:
        return templates.TemplateResponse(
            request, "register.html", {"user": None, "error": error, "email": email},
            status_code=400,
        )

    new_user = User(email=email, password_hash=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return redirect_with_cookie("/", new_user.id)  


@router.get("/login")
def login_page(request: Request, user: User | None = Depends(get_current_user_optional)):
    return templates.TemplateResponse(request, "login.html", {"user": user})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()
    found = db.scalar(select(User).where(User.email == email))
    if not found or not verify_password(password, found.password_hash):
        return templates.TemplateResponse(
            request, "login.html",
            {"user": None, "error": "Wrong email or password.", "email": email},
            status_code=400,
        )
    return redirect_with_cookie("/", found.id)


@router.post("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response