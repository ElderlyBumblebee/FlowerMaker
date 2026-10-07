from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.assistant.service import recommend
from src.auth.dependencies import get_current_user
from src.core.database import get_db
from src.core.models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

EXAMPLES = [
    "A bouquet for my grandmother's 80th birthday, up to €50",
    "Something to say sorry to my girlfriend, not too expensive",
    "A gift for a colleague, no strong scent, around €25",
]


@router.get("/assistant")
def assistant_page(
    request: Request,
    q: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),  
):
    result = recommend(db, q) if q and q.strip() else None
    return templates.TemplateResponse(
        request,
        "assistant.html",
        {"user": user, "q": q or "", "result": result, "examples": EXAMPLES},
    )