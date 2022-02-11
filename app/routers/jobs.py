from fastapi import APIRouter,HTTPException,status
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.functions import func
from typing import List

from app.schemas import Jobs_req, jobs_nes, jobs_res
from app.database import get_db
from app.oauth2 import  get_current_user
from app.models import Jobs, JobsApplied


router = APIRouter(prefix="/jobs",tags=["JOBS"])
@router.post("/create",response_model=jobs_res)
def create(request:Jobs_req,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    User_data = Jobs(posted_by=current_user.get("id"),**request.dict())
    if "Recruiter" == current_user.get("role"):
        db.add(User_data)
        db.commit()
        db.refresh(User_data)
        return User_data
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="YOU CANT POST THIS")


@router.get("/all",response_model=List[jobs_nes])
def getts(db:Session=Depends(get_db)):
    jobs= db.query(Jobs,func.count(JobsApplied.seeker_id).label("applied_for")).join(JobsApplied,isouter=True).group_by(Jobs.id).all()
    print(jobs)
    return jobs

@router.get("/get/{id}",response_model=jobs_res)
def get1(id:int,db:Session = Depends(get_db)):
    user = db.query(Jobs).filter(id==Jobs.id)
    user_id = user.first()
    if user_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"NO USER WITH ID : {id}")
    return user_id

@router.put("/update/{id}",response_model=jobs_res)
def fuun(id:int,request:Jobs_req,db:Session=Depends(get_db),current_user = Depends(get_current_user)):

    user = db.query(Jobs).filter(id==Jobs.id)
    user_id = user.first()
    pos_by = user_id.posted_by

    r_id = current_user.get("id")
    if r_id == pos_by:
        user = db.query(Jobs).filter(id==Jobs.id)
        uid = user.first()
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} does not exist")
        user.update(request.dict())
        db.commit()
        db.refresh(uid)
        return uid
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="U CANNOT UPDATE THID")

@router.delete("/del/{id}")
def fuun(id:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):

    user = db.query(Jobs).filter(id==Jobs.id)
    user_id = user.first()
    pos_by = user_id.posted_by

    r_id = current_user.get("id")
    if r_id == pos_by:
        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id}job does not exist")
        user.delete()
        db.commit()
        return "SUCCESSFULLY DELETED"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="U CANNOT DELETE THID")

