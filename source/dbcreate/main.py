import io
import os
import logging
import operator
import asyncio
import database as database
from appdb.models import User



async def on_startup():
    await database.start()


if __name__ == '__main__':
    asyncio.run(database.start())