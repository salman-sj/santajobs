from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from starlette import status

from app.database import get_db
from app.models import JobsApplied, Seekers
from app.oauth2 import  get_current_user



router = APIRouter(prefix="/applied",tags=["APPLIED"])

@router.post("/{id}")
def applied(id:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    if "Seeker"== current_user.get("role"):
        data = JobsApplied(
            job_id = id,
            seeker_id = current_user.get("id")
        )
        db.add(data)
        db.commit()
        return "COPPIED SUCCESSFULLY"
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cannot apply")