from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.assistant.router import router as assistant_router
from src.auth.dependencies import get_current_user_optional
from src.auth.router import router as auth_router
from src.cart.router import router as cart_router
from src.core.models import User
from src.orders.router import router as orders_router
from src.products.router import router as products_router

app = FastAPI(title="FlowerMaker")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(assistant_router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request, user: User | None = Depends(get_current_user_optional)):
    return templates.TemplateResponse(request, "home.html", {"user": user})