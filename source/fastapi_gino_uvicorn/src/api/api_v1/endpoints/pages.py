from typing import Any, List
from fastapi import APIRouter, Request
from schemas.models import User, UserCreate, UserUpdate
from models.models import User as ORMUser
from fastapi import Request,Response,Cookie,Form,FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from models.models import User as ORMUser
from models.models import Cookies as ORMCookies
app = FastAPI()
router = APIRouter()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")


@router.get('/start',response_class=HTMLResponse )
async def start(request: Request,response: Response,CookieId: Optional[str] = Cookie(None))-> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    print(check)
    if check == 504:
        response = templates.TemplateResponse('login.html',{"request":request})
        response.delete_cookie("CookieId")
        return response
