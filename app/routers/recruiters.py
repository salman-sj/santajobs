from fastapi import APIRouter,HTTPException,status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.models import Recruiters,Jobs,JobsApplied,Seekers,Selected
from app.oauth2 import generate_access_token, get_current_user
from app.schemas import rec_out, s_rec
from app.utils import hash,verify

router = APIRouter(prefix="/recruiters",tags=["RECRUITERS"])

@router.post("/create")
def create(request:s_rec,db:Session = Depends (get_db) ):
    request.password = hash(request.password)
    creating = Recruiters(**request.dict())
    db.add(creating)
    db.commit()
    db.refresh(creating)
    return creating

@router.get("/all",response_model=list[rec_out])
def get(db:Session = Depends(get_db)):
    return db.query(Recruiters).all()

@router.get("/get/{id}",response_model=rec_out)
def get(id:int,db:Session = Depends(get_db)):
    d=db.query(Recruiters).filter(id==Recruiters.id)
    iid=d.first()
    if not iid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id:{id} is not available")
    return iid


@router.put("/update/{id}",response_model=rec_out)
def update(id:int,request:rec_out,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    uid = current_user.get("id")
    if uid!=id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cant process this")
    d = db.query(Recruiters).filter(id==Recruiters.id)
    iid = d.first()
    if not iid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} does not exist")
    d.update(request.dict())
    db.commit()
    db.refresh(iid)
    return iid

@router.delete("/del/{id}")
def delt(id:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    uid = current_user.get("id")
    if uid!=id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cant process this")
    d = db.query(Recruiters).filter(id==Recruiters.id)
    iid = d.first()
    if not iid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"could not find id : {id}")
    d.delete()
    db.commit()
    return "succesfully Deleted"

@router.get("/dash",tags=["DASHBOARD"])
def das(db:Session=Depends(get_db),current_user : dict = Depends(get_current_user)):
    if current_user.get("role")!="Recruiter":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not Recruiter")
    applicant = db.query(
            Recruiters.c_name,
            Jobs.title,
            Seekers.id,
            Seekers.name,
            Seekers.email,
        ).join(Jobs, isouter=True).join(JobsApplied, isouter=True).join(Seekers, isouter=True).filter(Recruiters.id == current_user.get("id")).all()
    return applicant

@router.post("select/{jid}/{sid}")
def select(jid:int,sid:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    if "Recruiter"== current_user.get("role"):
        data = Selected(
            job_id = jid,
            seeker_id = sid
        )
        db.add(data)
        db.commit()
        return "Selected"
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not recruiter")




def verif(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(Recruiters).filter(request.username==Recruiters.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="could not find the user ")
    p=verify(request.password,user.password)
    if not p:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE NOT AUTHORIZED")
    token = generate_access_token({"id":user.id,"role":"Recruiter"})
    return {"access_token":token,"token_type":"bearer"}
