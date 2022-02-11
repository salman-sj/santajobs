from fastapi import FastAPI

from app.routers import recruiters
from app.routers import jobs
from app.routers import seekers
from app.routers import oauth
from app.routers import applied


app = FastAPI()

app.include_router(recruiters.router)
app.include_router(jobs.router)
app.include_router(seekers.router)
app.include_router(oauth.router)
app.include_router(applied.router)



@app.get("/hi")
def hello():
    return "hello world"