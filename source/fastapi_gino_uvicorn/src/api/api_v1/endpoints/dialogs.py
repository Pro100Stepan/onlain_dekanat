from typing import Any, List
from fastapi import APIRouter
from fastapi import Request,Response,Cookie,Form
from schemas.models import User, UserCreate, UserUpdate, Message,MessageBase
from models.models import User as ORMUser
from models.models import Messages as ORMMessages
from models.models import Dialogs as ORMDialogs
from gino import Gino
import os
db = Gino()


router = APIRouter()



@router.post('/')
async def get_or_create(
    request: Request,sender_1 = Form(...),sender_2 = Form(...)) -> Any:
    dialog :  ORMDialogs = await  ORMDialogs.get_or_create(sender_1,sender_2)
    return dialog
@router.post('/new_message')
async def up_message(request: Request ,sender_1 = Form(...),sender_2 = Form(...),message=Form(...)):
    message :ORMDialogs = await ORMDialogs.up_message(sender_1,sender_2,message)
    return message
@router.post('/get_messages')
async def get_message(sender_1 = Form(...),sender_2 = Form(...)) -> Any:
    messages: ORMDialogs = await ORMDialogs.get_dialog(sender_1,sender_2)
    return messages