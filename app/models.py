from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY, TIMESTAMP, Integer, String
from .database import Base
from sqlalchemy import Column


class Recruiters(Base):
    __tablename__ = "Recruiters"
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    c_name = Column(String,nullable=False)
    id = Column(Integer,primary_key=True,nullable=False)
    jobs = relationship("Jobs",back_populates="recruiter")



class Jobs(Base):
    __tablename__ = "Jobs"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    describtion = Column(String,nullable=False)
    posted_by = Column(Integer,ForeignKey("Recruiters.id",ondelete="CASCADE"),nullable=False)
    posted_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    eligibility = Column(String,nullable=False)
    location = Column(String,nullable=False)
    job_type = Column(String,nullable=False)
    level = Column(String,nullable=True)
    recruiter = relationship("Recruiters",back_populates="jobs")

class Seekers(Base):
    __tablename__ = "Seekers"
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    resume = Column(String,nullable=False)
    level = Column(String,nullable=True)
    portfolio = Column(String,nullable=True)
    job_field = Column(String,nullable=False)

class JobsApplied(Base):
    __tablename__ = "Jobs_Applied"
    id = Column(Integer,primary_key=True,nullable=False)
    job_id = Column(Integer,ForeignKey("Jobs.id",ondelete="CASCADE"),nullable=False)
    seeker_id = Column(Integer,ForeignKey("Seekers.id",ondelete="CASCADE"),nullable=False)


class Selected(Base):
    __tablename__ = "Selected"
    id = Column(Integer,primary_key=True,nullable=False)
    job_id = Column(Integer,ForeignKey("Jobs.id",ondelete="CASCADE"),nullable=False)
    seeker_id = Column(Integer,ForeignKey("Seekers.id",ondelete="CASCADE"),nullable=False)
    