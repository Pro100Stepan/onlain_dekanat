from gino import Gino
import os
db = Gino()


async def start():
    await db.set_bind(f"postgresql://%s:%s@db:%s/%s" % (os.environ.get("POSTGRESS_USER"), os.environ.get("POSTGRESS_PASSWORD"), os.environ.get("POSTGRESS_DB_PORT"), os.environ.get("POSTGRESS_DB_NAME")))
    # Create tables
    await db.gino.create_all()
