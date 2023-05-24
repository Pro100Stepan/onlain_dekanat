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

from fastapi.param_functions import Query
from models.models import User as ORMUser
from models.models import Cookies as ORMCookies
from models.models import Zachetka as ORMZachetka
from models.models import Notes as ORMNotes
from models.models import Subject as ORMSubject
app = FastAPI()
router = APIRouter()
from gino import Gino
import os


db = Gino()
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
@router.post('/crateSubject')
async def createSubject(teacher=Form(...),group=Form(...),subject=Form(...))-> Any:
    create_subject: ORMSubject = await ORMSubject.create_s(teacher,group,subject)
    return create_subject

@router.post('/get_group')
async def get_group(id,CookieId: Optional[str] = Cookie(None)) -> Any:
    request= Request
    response= Response
    get_group: ORMSubject = await ORMSubject.get_students(id=id)
    return get_group
@router.post('/get_subjects')#надо убрать teacher его будем узнавать по кукам 
async def get_subjects(teacher,CookieId: Optional[str] = Cookie(None)) -> Any:
    request= Request
    response= Response
    get_subjects: ORMSubject = await ORMSubject.get_subjects(teacher = teacher)
    return get_subjects
@router.post('/crateNote')
async def create(zachetkaid,teacher,subject,semestr,note)-> Any:
    note : ORMNotes = await ORMNotes.create_note(zachetkaid,teacher,subject,semestr,note)
    return note
@router.get('/get_my_notes')
async def get_my_notes(CookieId: Optional[str] = Cookie(None))-> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    check = check.__dict__
    value = check["__values__"]
    userId = value['userId']
    #return userId
    zachetkaid: ORMZachetka = await ORMZachetka.query.where(ORMZachetka.userId == userId).gino.first()
    zachetkaid = zachetkaid.id
    # zachetkaid : ORMZachetka = await ORMZachetka.get_zachetka_userId(userId = userId)
    # zachetkaid = zachetkaid.__dict__
    # zachetkaid = zachetkaid["__values__"]
    # zachetkaid = zachetkaid["id"]
    my_notes: ORMNotes = await ORMNotes.get_notes_of_zachetka(zachetkaid = int(zachetkaid))
    return my_notes