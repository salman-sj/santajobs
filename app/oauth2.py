from datetime import datetime, timedelta
from fastapi import HTTPException , status
from fastapi.params import Depends
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from app.env_settings import setting
from app.database import get_db

ALGORITHM = setting.ALGORITHM
SECRETE_KEY = setting.SECRET_KEY
EXPIRY_MINUTES = setting.EXPIRE_TIME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_access_token(data: dict):
    to_encode = data.copy()
    expiry_minutes = datetime.utcnow()+timedelta(minutes=EXPIRY_MINUTES)
    to_encode.update({"exp":expiry_minutes})
    token = jwt.encode(to_encode,SECRETE_KEY,ALGORITHM)
    return token

def verify_access_token(token,credential_exception):
    try:
        token_data = jwt.decode(token=token,key=SECRETE_KEY,algorithms=[ALGORITHM])
        print(token_data)
        user_id = token_data.get("id")
        if user_id==None:
            raise credential_exception

    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token=Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDENTIAL",headers={"WWW-AUTHENTICATE":"BEAREAR"})
    token_data=verify_access_token(token,credential_exception)
    return token_data
     