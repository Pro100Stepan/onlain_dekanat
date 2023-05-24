from fastapi import APIRouter


from models.models import User as ORMUser


from .endpoints import dialogs, users, pages, ws, students_submissions, zachetka
admin: ORMUser = ORMUser.get_user_for_email(email = "admin")

pagesRouter = APIRouter()
usersRouter = APIRouter()
cloudsRouter = APIRouter()
wsRouter = APIRouter()
dialogsRouter = APIRouter()
submissionsRouter = APIRouter()
zachetkaRouter = APIRouter()
cloudsRouter.include_router(router=ws.router,prefix="")
pagesRouter.include_router(router=pages.router,prefix="")
usersRouter.include_router(router=users.router,prefix="/users")
submissionsRouter.include_router(router=students_submissions.router,prefix="/submissions")
dialogsRouter.include_router(router=dialogs.router,prefix="/dialogs")
zachetkaRouter.include_router(router=zachetka.router,prefix="/zachetka")

