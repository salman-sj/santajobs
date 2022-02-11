from pydantic import BaseSettings

class Sett(BaseSettings):
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    ALGORITHM: str
    SECRET_KEY: str
    EXPIRE_TIME: int

setting = Sett(_env_file=".env")