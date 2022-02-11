from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime
from typing import List

from starlette import responses
class s_rec(BaseModel):
    email : EmailStr
    password : str
    c_name : str
    
class jobs_rel(BaseModel):
    id : int
    title : str
    posted_at : datetime
    posted_by : int
    describtion : str
    eligibility : str
    location: str
    job_type : str
    level : str
    class Config:
        orm_mode = True
    
class rec_out(BaseModel):
    id : int
    email : EmailStr
    c_name : str
    jobs : List[jobs_rel]
    class Config:
        orm_mode = True
class rec_rel(BaseModel):
    id : int
    email : EmailStr
    c_name : str
    class Config:
        orm_mode = True

class dash(BaseModel):
    id : int
    email : EmailStr
    c_name : str
    jobs : List[jobs_rel]
    
    class Config:
        orm_mode = True

#recruiter end jobs start

class Jobs_req(BaseModel):
    title : str
    describtion : str
    eligibility : str
    location: str
    job_type : str
    level : str


class jobs_res(BaseModel):
    
    id : int
    title : str
    posted_at : datetime
    posted_by : int
    describtion : str
    eligibility : str
    location: str
    job_type : str
    level : str
    recruiter : rec_rel
    class Config:
        orm_mode = True

class jobs_nes(BaseModel):
    Jobs : jobs_res
    applied_for : int

    class Config:
        orm_mode = True

#seekers starts

class Seekers_req(BaseModel):
    name : str
    email : EmailStr
    password : str
    resume : str
    level : str
    portfolio : str
    job_field : str

class Seekers_res(BaseModel):
    id : int
    name : str
    email : EmailStr
    resume : str
    level : str
    portfolio : str
    job_field : str
    class Config:
        orm_mode = True

