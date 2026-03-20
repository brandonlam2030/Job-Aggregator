from fastapi import Depends, FastAPI
import requests,time
from . import models
from .database import engine, SessionLocal
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware


class JobInfo(BaseModel):
    Company:str
    Role:str
    Date_Found:datetime
    Location:str
    Link:str

    class Config:
        from_attributes = True

class JobDescription(BaseModel):
    url:str



def getLink(url:str):
    temp = url.split("/")
    company = temp[2].split(".")[0]
    return temp[0] + "//" + temp[2] + "/wday/cxs/" + company + "/" + temp[4] + "/" + temp[5] + "/" + temp[6] + "/" + temp[7]

headers = {
    "Content-Type": "application/json"
}


app = FastAPI()
models.Base.metadata.create_all(bind = engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def start_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/jobs", response_model = list[JobInfo])
def get_jobs(session: requests.Session = Depends(start_db), limit:int = 10, offset:int = 0):
    return session.execute(select(models.Job).limit(limit).offset(offset).order_by(models.Job.Date_Found.desc())).scalars().all()

@app.get("/jobs/{search}",response_model = list[JobInfo])
def get_specific_job(company: str, session: requests.Session = Depends(start_db), limit:int = 10, offset:int = 0):
    return session.execute(select(models.Job).where(models.Job.Company.ilike(company)).limit(limit).offset(offset).order_by(models.Job.Date_Found.desc())).scalars().all()

@app.post("/jobs/description")
def get_description(body: JobDescription):
    url = getLink(body.url)
    print(url)
    for attempt in range(3):
        try:
            resp = requests.get(url, headers= headers, timeout = 10)

            if resp.status_code != 200:
                break
            
            try:
                res = resp.json()
            except: 
                break
            
            if "jobPostingInfo" not in res:
                break
            return BeautifulSoup(res["jobPostingInfo"]["jobDescription"], "html.parser").get_text(strip = True, separator = " ")
            
        except requests.RequestException: time.sleep(2)
