from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user_optional
from src.core.database import get_db
from src.core.models import Product, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

MESSAGES = {
    "added": "Added to cart.",
    "unavailable": "Sorry, this product is out of stock.",
}


@router.get("/catalog")
def catalog(
    request: Request,
    msg: str | None = None,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    products = db.scalars(
        select(Product).order_by((Product.stock == 0), Product.name)
    ).all()
    return templates.TemplateResponse(
        request,
        "catalog.html",
        {"user": user, "products": products, "message": MESSAGES.get(msg)},
    )