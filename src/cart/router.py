from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.auth.dependencies import get_current_user
from src.core.database import get_db
from src.core.models import CartItem, Product, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

MESSAGES = {
    "stock_changed": "Some items were no longer available in the quantity you wanted. "
    "We updated your cart, please check it and try again.",
}


@router.get("/cart")
def cart_page(
    request: Request,
    msg: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items = db.scalars(
        select(CartItem)
        .where(CartItem.user_id == user.id)
        .options(joinedload(CartItem.product))
        .order_by(CartItem.id)
    ).all()
    total = sum((i.product.price * i.quantity for i in items), Decimal("0"))
    return templates.TemplateResponse(
        request,
        "cart.html",
        {"user": user, "items": items, "total": total, "message": MESSAGES.get(msg)},
    )


@router.post("/cart/add")
def add_to_cart(
    product_id: int = Form(...),
    quantity: int = Form(1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user), 
):
    product = db.get(Product, product_id)
    if product is None or product.stock <= 0:
        return RedirectResponse("/catalog?msg=unavailable", status_code=303)

    quantity = max(1, quantity)
    item = db.scalar(
        select(CartItem).where(
            CartItem.user_id == user.id, CartItem.product_id == product_id
        )
    )
    if item:
        item.quantity = min(item.quantity + quantity, product.stock)
    else:
        db.add(
            CartItem(
                user_id=user.id,
                product_id=product_id,
                quantity=min(quantity, product.stock),
            )
        )
    db.commit()
    return RedirectResponse("/catalog?msg=added", status_code=303)


@router.post("/cart/update")
def update_cart_item(
    item_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = db.scalar(
        select(CartItem)
        .where(CartItem.id == item_id, CartItem.user_id == user.id)
        .options(joinedload(CartItem.product))
    )
    if item:
        new_quantity = min(quantity, item.product.stock)
        if new_quantity <= 0:
            db.delete(item)
        else:
            item.quantity = new_quantity
        db.commit()
    return RedirectResponse("/cart", status_code=303)


@router.post("/cart/remove")
def remove_cart_item(
    item_id: int = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = db.scalar(
        select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user.id)
    )
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse("/cart", status_code=303)