from fastapi import APIRouter,status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.params import Depends
from sqlalchemy.orm import session
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.models import Seekers
from app.oauth2 import generate_access_token, get_current_user

from app.schemas import Seekers_req, Seekers_res
from app.utils import verify,hash


router = APIRouter(prefix="/seeker",tags=["Seekers"])
@router.post("/create",response_model=Seekers_res)
def create(request:Seekers_req,db:Session = Depends(get_db)):
    request.password = hash(request.password)
    data = Seekers(**request.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.get("/all",response_model=list[Seekers_res])
def get_all(db:Session=Depends(get_db)):
    return db.query(Seekers).all()

@router.get("/get/{id}",response_model=Seekers_res)
def get_one(id:int,db:Session=Depends(get_db)):
    user = db.query(Seekers).filter(id==Seekers.id)
    get = user.first()
    if get == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Nai hae ba apka user")
    else:
        return get

@router.put("/update/{id}",response_model=Seekers_res)
def update(id:int,request:Seekers_req,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    u_id = current_user.get("id")
    if u_id!=id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cant process this")
    user = db.query(Seekers).filter(id==Seekers.id)
    u_id = user.first()
    user.update(request.dict())
    db.commit()
    db.refresh(u_id)
    return u_id

@router.delete("/del/{id}")
def dele(id:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    uid = current_user.get("id")
    if uid!=id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cant process this")
    user = db.query(Seekers).filter(id==Seekers.id)
    iid = user.first()
    if not iid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"could not find id : {id}")
    user.delete()
    db.commit()
    return "DELETED"


def verif(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(Seekers).filter(request.username ==Seekers.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="could not find the user ")
    p=verify(request.password,user.password)
    if not p:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE NOT AUTHORIZED")
    token = generate_access_token({"id":user.id,"role":"Seeker"})
    return {"access_token":token,"token_type":"bearer"}