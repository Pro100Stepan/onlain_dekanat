from gino import Gino
import os
db = Gino()
from models.models import User as ORMUser

async def start():
    await db.set_bind(f"postgresql://%s:%s@db:%s/%s" % (os.environ.get("POSTGRESS_USER"), os.environ.get("POSTGRESS_PASSWORD"), os.environ.get("POSTGRESS_DB_PORT"), os.environ.get("POSTGRESS_DB_NAME")))
    # Create tables
    await db.gino.create_all()
admin: ORMUser = ORMUser.get_user_for_email(email = "admin")
if admin is None:
    create_admin: ORMUser = ORMUser.create_user(login="admin",email="admin",phone="admin",role="admin",name="admin",admission_year="admin",course=1,direction="admin",group='admin',hostel='admin',password='admin',zachetkaid="admin")

start()