from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.auth.dependencies import get_current_user
from src.core.database import get_db
from src.core.models import CartItem, Order, OrderItem, Product, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/orders/checkout")
def checkout(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items = db.scalars(
        select(CartItem).where(CartItem.user_id == user.id).order_by(CartItem.id)
    ).all()
    if not items:
        return RedirectResponse("/cart", status_code=303)

    product_ids = sorted({item.product_id for item in items})
    locked = db.scalars(
        select(Product)
        .where(Product.id.in_(product_ids))
        .order_by(Product.id)
        .with_for_update()
    ).all()
    products = {p.id: p for p in locked}

    stock_problem = False
    for item in items:
        product = products[item.product_id]
        if item.quantity > product.stock:
            stock_problem = True
            if product.stock <= 0:
                db.delete(item)
            else:
                item.quantity = product.stock
    if stock_problem:
        db.commit()
        return RedirectResponse("/cart?msg=stock_changed", status_code=303)

    order = Order(user_id=user.id, status="confirmed", total=Decimal("0"))
    total = Decimal("0")
    for item in items:
        product = products[item.product_id]
        order.items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price_at_purchase=product.price,  
            )
        )
        product.stock -= item.quantity
        total += product.price * item.quantity
        db.delete(item)  
    order.total = total

    db.add(order)
    db.commit()  
    return RedirectResponse(f"/orders/{order.id}?placed=1", status_code=303)


@router.get("/orders")
def orders_page(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    orders = db.scalars(
        select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        request, "orders.html", {"user": user, "orders": orders}
    )


@router.get("/orders/{order_id}")
def order_detail(
    order_id: int,
    request: Request,
    placed: int = 0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = db.scalar(
        select(Order)
        .where(Order.id == order_id, Order.user_id == user.id)
        .options(selectinload(Order.items).joinedload(OrderItem.product))
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return templates.TemplateResponse(
        request,
        "order_detail.html",
        {"user": user, "order": order, "placed": bool(placed)},
    )