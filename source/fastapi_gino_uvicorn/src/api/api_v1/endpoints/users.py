import argparse
import sys
from typing import List


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
db = Gino()
from uuid import uuid4
import requests


from fastapi.templating import Jinja2Templates
router = APIRouter()
templates = Jinja2Templates(directory="./templates")

import hashlib

@router.get("/create_admin")
async def create_admin() -> Any:
    admin: ORMUser = await ORMUser.get_user_for_email(email = "admin")
    #return admin.__dict__
    if admin is None:
      
        create_admin: ORMUser = await ORMUser.create_user(login="admin",email="admin",phone="admin",role="admin",name="admin",admission_year="admin",course=1,direction="admin",group='admin',hostel='admin',password='admin',zachetkaid="admin")
        return admin
    else:
        return

# @router.get("/cookies")
# async def read_cookies() -> Any:
#     cookies = await ORMCookies.query.gino.all()
#     return cookies
# @router.get("/cookies/delete")
# async def delete_cookies()  -> Any:
#     return await ORMCookies.delete_not_valid_token()
@router.get('/', response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
        Retrieve users.
    """
    users = await ORMUser.query.gino.all()
    return users


@router.get('/main',response_class=HTMLResponse )
async def main(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)):
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
        return response 
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        if check == 504:
            response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
            return response 
        else:
            check = check.__dict__
            value = check["__values__"]
            userId = value['userId']
            role : ORMUser = await ORMUser.get_role(username = userId)
            if role == 'admin':
                return templates.TemplateResponse('main_admin.html',{"request":request})
            else:
                return templates.TemplateResponse('main.html',{"request":request})



@router.post('/useradd',response_class=HTMLResponse )
async def useradd_admin(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)):
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        role : ORMUser = await ORMUser.get_role(username = userId)
        if role == 'admin':
            return templates.TemplateResponse('useradd.html',{"request":request})
        else:
            return '404'






@router.get('/status_dopusk',response_class=HTMLResponse )
async def main(request: Request,response: Response):
    dopusk=request.get('http://localhost:80/v1/submissions/get_my_dopusk')
    return templates.TemplateResponse('status_dopusk.html',{"request":request,'dopusk':dopusk})





@router.get('/start',response_class=HTMLResponse )
async def start(request: Request,response: Response,CookieId: Optional[str] = Cookie(None))-> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    status = response.status_code
    if check == 504:
        response = templates.TemplateResponse('login.html',{"request":request})
        response.delete_cookie("CookieId")
        return response
    else:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)
        return response
@router.get('/login_false',response_class=HTMLResponse )
async def main(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)) -> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    status = response.status_code
    if check == 504:
        return templates.TemplateResponse('login_false.html',{"request":request})
        response.delete_cookie("CookieId")
        return response
    else:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)
        return response
    

@router.post('/login',response_class=HTMLResponse )
async def login(email = Form(...),password = Form(...),CookieId: Optional[str] = Cookie(None)) -> Any:
    password = hashlib.sha256(password.encode())
    password=str(password.hexdigest())
    response= Response
    request = Request
    if CookieId is None:
        check : ORMUser = await ORMUser.check_password(email,password)
        username = email
        if check is True:
            value = str(uuid4()).replace('-', '')
            add_cookies : ORMCookies = await ORMCookies.get_or_create(userId=username,value=value)
            print(add_cookies.__dict__)
            response =  RedirectResponse(
                'http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)
            response.set_cookie(key="CookieId", value=value)
            return response
        else:
            return RedirectResponse('http://localhost:80/v1/users/login_false',  status_code=status.HTTP_302_FOUND)
    elif CookieId is not None:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        if check == 504:
            return RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
        else:
            response =  RedirectResponse('http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)
            return response
@router.get('/login/desauth')
async def desauth(request: Request,response: Response,CookieId: Optional[str] = Cookie(None)) -> Any:
    response =  RedirectResponse('http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    response.delete_cookie("CookieId")
    delete : ORMCookies = await ORMCookies.delete_cookie(value=CookieId)
    return response



# @router.get('/login_test/{username}')
# async def test_login(username: str,password:str ,response: Request)-> Any:
#     check : ORMUser = await ORMUser.check_password(email=username,password=password)
#     if check is True:
#         value = str(uuid4()).replace('-', '')
#         content= 'yess'
#         response = JSONResponse(content=content)
#         add_cookies : ORMCookies(userId=username,value=value)
#         response.set_cookie(key="CookieId",value=value)

#         return response
#     else:
#         return requests.get("http://localhost:80/v1/users/start")

@router.get('/test_working')
async def read_cookies(CookieId: Optional[str] = Cookie(None)) -> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    if check == 504:
        return RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
    name = check.userId
    return name

@router.post('/create_user')
async def create_user(login = Form(...),email = Form(...),phone = Form(...), role = Form(...),name = Form(...),admission_year = Form(...),
    course = Form(...),direction = Form(...),group =Form(...),hostel = Form(...),password = Form(...),zachetkaid=Form(...),CookieId: Optional[str] = Cookie(None)) -> Any:
    #new_user : ORMUser = await ORMUser.create_user(login,email,phone,role,name,admission_year,int(course),direction,group,hostel,password,zachetkaid)
  
    response= Response
    if CookieId is None:
        response =  RedirectResponse(
            'http://localhost:80/v1/users/start',  status_code=status.HTTP_302_FOUND)
        return response
    else:
        check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
        if check == 504:
            return RedirectResponse(
             'http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)
        check = check.__dict__
        value = check["__values__"]
        userId = value['userId']
        role_user : ORMUser = await ORMUser.get_role(username = userId)
        if role_user == 'admin':
            new_user : ORMUser = await ORMUser.create_user(login,email,phone,role,name,admission_year,int(course),direction,group,hostel,password,zachetkaid)


            return RedirectResponse(
             'http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)
        else:
            return RedirectResponse(
             'http://localhost:80/v1/users/main',  status_code=status.HTTP_302_FOUND)




@router.put('/{id}', response_model=User)
async def update_user(
    id: int,
    request: UserUpdate
) -> Any:
    """
    Update user
    """
    user : ORMUser= await ORMUser.get_or_404(id)
    updated_fields : User = User.from_orm(request)
    await user.update(**updated_fields.dict(skip_defaults=True)).apply()
    return User.from_orm(user)









async def check_cookie(CookieId) -> Any:
    check : ORMCookies = await ORMCookies.get_cookie(value=CookieId)
    check = check.__dict__
    value = check["__values__"]
    userId = value['userId']
    role : ORMUser = await ORMUser.get_role(username = userId)
