import argparse
import sys



from typing import Any, List
from fastapi import APIRouter
from fastapi.param_functions import Query
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi import Request,Response,Cookie,Form
from typing import Optional
from starlette import responses
import starlette.status as status

from starlette.responses import HTMLResponse
from schemas.models import User, UserCreate, UserUpdate, UserLogin
from models.models import User as ORMUser
from models.models import Cookies as ORMCookies
from gino import Gino
import os
from models.models import Dopusk_submissions as ORMDopusk_submissions
from models.models import Spravka_submissions as ORMSpravka_submissions
from datetime import date,datetime

from fastapi import Request,Response,Cookie,Form

from fastapi.templating import Jinja2Templates
db = Gino()


router = APIRouter()


templates = Jinja2Templates(directory="./templates")

@router.get('/create_spravka',response_class=HTMLResponse )
async def main(request: Request,response: Response):
    return templates.TemplateResponse('create_spravka.html',{"request":request})

@router.get('/create_dopusk',response_class=HTMLResponse )
async def main(request: Request,response: Response):
    return templates.TemplateResponse('create_dopusk.html',{"request":request})

@router.get('/create_dopusk_accept',response_class=HTMLResponse )
async def main(request: Request,response: Response):
    return templates.TemplateResponse('create_dopusk_accept.html',{"request":request})

@router.get('/create_spravka_accept',response_class=HTMLResponse )
async def main(request: Request,response: Response):
    return templates.TemplateResponse('create_spravka_accept.html',{"request":request})


@router.post('/dopusk')
async def create_dopusk(CookieId: Optional[str] = Cookie(None), teacher =Form(...), subject = Form(...),status_author="-",semestr = Form(...)) -> Any:
    request= Request
    response= Response
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        student = value['userId']
        student = str(student)
        student = await ORMUser.get_name(email = student)
        submission = await ORMDopusk_submissions.get_or_create_dopusk(student,subject,teacher,status_author,int(semestr))
        response =  RedirectResponse('http://localhost/v1/submissions/create_dopusk_accept',  status_code=status.HTTP_302_FOUND)
        return response

@router.post('/spravka')
async def create_spravka(CookieId: Optional[str] = Cookie(None),way_point=Form(...), quantity=Form(...)) -> Any:
    request= Request
    response= Response
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        student = value['userId']
        student = str(student)
        student = await ORMUser.get_name(email = student)
        submission = await ORMSpravka_submissions.get_or_create_spravka(student,way_point,int(quantity),'-')
        response =  RedirectResponse('http://localhost/v1/submissions/create_spravka_accept',  status_code=status.HTTP_302_FOUND)
        return response

@router.get("/get_dopusk")
async def get():
    pop = await ORMDopusk_submissions.query.gino.all()
    return pop

@router.post('/update__dopusk_status')
async def update_status(student , teacher , subject , new_status , status_author ) -> Any:
    status = await ORMDopusk_submissions.update_status(student,subject,teacher,new_status,status_author)
    return status

@router.get("/get_spravka")
async def get():
    pop = await ORMSpravka_submissions.query.gino.all()
    return pop

@router.post('/update_spravka_status')
async def update_status(student , way_point , quantity ,new_status ,status_author ) -> Any:
    status = await ORMSpravka_submissions.update_status(student,way_point,int(quantity),new_status,status_author)
    return status

@router.get('/status_dopusk',response_class=HTMLResponse )
async def main(request: Request,response: Response):
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        user: ORMUser = await ORMUser.get_user_for_email(email = userId)
        user = user.__dict__
        value = user['__values__']
        name = value['name']
        dopusk: ORMDopusk_submissions = await ORMDopusk_submissions.get_dopusk_of_user(student = name)
    return templates.TemplateResponse('status_dopusk.html',{"request":request})

@router.get('/viev_dopusk/{id}',response_class=HTMLResponse )
async def main(request: Request, response: Response, id: str):
    #id- id Допуска который нужен нам для редактирования
    dopusk: ORMDopusk_submissions =  await ORMDopusk_submissions.get(int(id))
    dopusk = dopusk.__dict__
    return templates.TemplateResponse('edit_dopusk.html',{"request":request,"dopusk":dopusk,"id":id})

@router.get('/viev_spravka/{id}',response_class=HTMLResponse )
async def main(request: Request, response: Response, id: str):
    #id- id Допуска который нужен нам для редактирования
    # Нужно вытаскивать допуск по id
    spravka: ORMSpravka_submissions = await ORMSpravka_submissions.get(int(id))
    spravka = spravka.__dict__
    return templates.TemplateResponse('edit_spravka.html',{"request":request, "spravka":spravka, "id":id})

@router.post('/edit_spravka/{id}',response_class=HTMLResponse )
async def main(request: Request, response: Response, id: int,new_status=Form(...),CookieId: Optional[str] = Cookie(None)):
    # id- id допуска/справки

    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
        return response 
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        role : ORMUser = await ORMUser.get_role(username = userId)
        if role == 'admin':
            spravka : ORMSpravka_submissions = await ORMSpravka_submissions.update_status(id=id,new_status=new_status)
            response =  RedirectResponse(
            'http://localhost:80/v1/submissions/get_my_spravka',  status_code=status.HTTP_302_FOUND)
            return response 
    

@router.post('/edit_dopusk/{id}',response_class=HTMLResponse )
async def main(request: Request, response: Response, id: int,new_status=Form(...),CookieId: Optional[str] = Cookie(None)):
    # id- id допуска/справки
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
        return response 
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        role : ORMUser = await ORMUser.get_role(username = userId)
        if role == 'admin':
            dopusk : ORMDopusk_submissions = await ORMDopusk_submissions.update_status(id=id,new_status=new_status)
            response =  RedirectResponse(
            'http://localhost:80/v1/submissions/get_my_dopusk',  status_code=status.HTTP_302_FOUND)
            return response 
    



@router.get('/get_my_dopusk')
async def get_dopusk(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)) -> Any:
    #Нужна проверка куки. Если админ, то status_dopusk_admin.html,
    # иначе status_dopusk.html Нужно вытаскивать все справки или сделать отдельный метод
    # туда надо передавать в такомже формате
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        role : ORMUser = await ORMUser.get_role(username = userId)
        if role == 'student':
            
            user: ORMUser = await ORMUser.get_user_for_email(email = userId)
            user = user.__dict__
            value = user['__values__']
            name = value['name']
            dopusk: ORMDopusk_submissions = await ORMDopusk_submissions.get_dopusk_of_user(student = name)
            dopusk_dict = {}
            s = 1
            for i in dopusk:
                dopusk = i.__dict__
                values = dopusk["__values__"]
                dopusk_dict[s] = values
                s +=1
            return templates.TemplateResponse('status_dopusk.html',{"request":request,'dopusk':dopusk_dict})
        elif role == 'admin':
            dopusk: ORMDopusk_submissions = await ORMDopusk_submissions.get_all()
            dopusk_dict = {}
            s = 1
            for i in dopusk:
                dopusk = i.__dict__
                values = dopusk["__values__"]
                dopusk_dict[s] = values
                s +=1
            return templates.TemplateResponse('status_dopusk_admin.html',{"request":request,'dopusk':dopusk_dict})

@router.get('/get_my_spravka',response_class=HTMLResponse )
async def get_status(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)):
    #Нужна проверка куки. Если админ, то status_spravka_admin.html,
    # иначе status_spravka.html. Нужно вытаскивать все допуски или сделать отдельный метод
    # туда надо передавать в такомже формате
    if CookieId is None:
        response =  RedirectResponse('http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        role : ORMUser = await ORMUser.get_role(username = userId)
        if role == 'student':
            user: ORMUser = await ORMUser.get_user_for_email(email = userId)
            user = user.__dict__
            value = user['__values__']
            name = value['name']
            spravka: ORMSpravka_submissions = await ORMSpravka_submissions.get_spravka_of_user(student = name)
            spravka_dict = {}
            s = 1
            for i in spravka:
                spravka = i.__dict__
                values = spravka["__values__"]
                spravka_dict[s] = values
                s +=1
            return templates.TemplateResponse('status_spravka.html',{"request":request,'spravka':spravka_dict})
        elif role == 'admin':
            spravka: ORMSpravka_submissions = await ORMSpravka_submissions.get_all()
            spravka_dict = {}
            s = 1
            for i in spravka:
                spravka = i.__dict__
                values = spravka["__values__"]
                spravka_dict[s] = values
                s +=1
            return templates.TemplateResponse('status_spravka_admin.html',{"request":request,'spravka':spravka_dict})