from fastapi import FastAPI,Request,Response,Cookie,Form
from typing import Optional
from custom_logging import CustomizeLogger
from core.config import settings
from fastapi.staticfiles import StaticFiles
from gino.ext.starlette import Gino
from pathlib import Path
import logging
import os

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

config_path=Path(__file__).with_name("logging_config.json")

templates = Jinja2Templates(directory="./templates")

app : FastAPI = FastAPI(title=settings.PROJECT_NAME,version=settings.VERSION)
logger = CustomizeLogger.make_logger(config_path)
app.logger = logger
app.mount("/static", StaticFiles(directory="static"), name="static")
db : Gino = Gino(dsn=settings.get_postgres_dsn())

db.init_app(app)



# @app.middleware("http")
# async def check_cookies(request:Request,call_next):
#     cookie_token: str = request.cookies.get("CookieId")
#     if cookie_token is None:
#         response = await call_next(request)
#         return response
#     elif cookie_token:
#         response = templates.TemplateResponse('login.html',{"request":request})
#         return response

    # The auth cookie is split toЯ ensure JS doesn't have full access (http_only), so we have to recreate it
    
    
from api.api_v1.api import usersRouter, pagesRouter, submissionsRouter,dialogsRouter,zachetkaRouter

app.include_router(usersRouter, prefix=settings.API_VERSION_STR, tags=['Users'])

app.include_router(pagesRouter, prefix=settings.API_VERSION_STR, tags=['Pages'])

app.include_router(dialogsRouter, prefix=settings.API_VERSION_STR, tags=['Dialogs'])

app.include_router(submissionsRouter, prefix=settings.API_VERSION_STR, tags=['Submissions'])

app.include_router(zachetkaRouter, prefix=settings.API_VERSION_STR, tags=['Zachetka'])