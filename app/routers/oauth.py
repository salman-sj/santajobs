





from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.models import Recruiters
from app.routers import recruiters as rec
from app.routers import seekers as sec
router = APIRouter(prefix="/login")

@router.post("")
def authorize(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    userr = request.username
    do = db.query(Recruiters).filter(userr==Recruiters.email).first()
    if do :
        print("idr toh aara in")
        return rec.verif(request,db)
    else:
        return sec.verif(request , db)
