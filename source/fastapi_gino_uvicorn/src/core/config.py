from pydantic import BaseSettings
import os
# from sqlalchemy.engine.url import URL

class Settings(BaseSettings):
    API_VERSION_STR : str = "/v1"
    PROJECT_NAME : str = "Fastapi-gino-uvicorn"
    VERSION: str = "0.0.0"

    # POSTGRES_SERVER: str = "lallah.db.elephantsql.com"
    # POSTGRES_USER: str = "qifealev"
    # POSTGRES_PASSWORD: str = "tnmtOSFsY0yf46nLNcoF_Q3QKVRTkVuF"
    # POSTGRES_DB: str = "qifealev"
    # POSTGRES_PORT: int = 5432

    class Config:
        case_sensitive = True
    
    def get_postgres_dsn(self):
        return (f"asyncpg://%s:%s@db:%s/%s" % (os.environ.get("POSTGRESS_USER"), os.environ.get("POSTGRESS_PASSWORD"), os.environ.get("POSTGRESS_DB_PORT"), os.environ.get("POSTGRESS_DB_NAME"))) #{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    def get_alembic_dsn(self):
        return (f"postgresql://%s:%s@db:%s/%s" % (os.environ.get("POSTGRESS_USER"), os.environ.get("POSTGRESS_PASSWORD"), os.environ.get("POSTGRESS_DB_PORT"), os.environ.get("POSTGRESS_DB_NAME")))#postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()