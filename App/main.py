import requests, time
from requests.exceptions import ConnectionError, Timeout
from . import models
from .database import engine, SessionLocal

headers = {"Content-Type": "application/json"}
payload = {
    "appliedFacets":{},
    "limit":20,
    "offset":0,
    "searchText": "computer science intern",
    "totalSelectedFacetsCount": 0
}

workday_companies = {
    #Big Tech
    "Nvidia": "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs",
    "Intel": "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
    "Salesforce": "https://salesforce.wd12.myworkdayjobs.com/wday/cxs/salesforce/External_Career_Site/jobs",
    "Dell": "https://dell.wd1.myworkdayjobs.com/wday/cxs/dell/External/jobs",
    "HPE": "https://hpe.wd5.myworkdayjobs.com/wday/cxs/hpe/Jobsathpe/jobs",
    "Micron": "https://micron.wd1.myworkdayjobs.com/wday/cxs/micron/External/jobs",
    "ADI": "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs",
    "Broadcom":"https://broadcom.wd1.myworkdayjobs.com/wday/cxs/broadcom/External_Career/jobs",
    "Global Foundries":"https://globalfoundries.wd1.myworkdayjobs.com/wday/cxs/globalfoundries/External/jobs",
    "Marvell": "https://marvell.wd1.myworkdayjobs.com/wday/cxs/marvell/MarvellCareers/jobs",
    "NXP": "https://nxp.wd3.myworkdayjobs.com/wday/cxs/nxp/careers/jobs",
    "Microchip": "https://wd5.myworkdaysite.com/wday/cxs/microchiphr/External/jobs",
    "Boeing": "https://boeing.wd1.myworkdayjobs.com/wday/cxs/boeing/EXTERNAL_CAREERS/jobs",
    "RTX": "https://globalhr.wd5.myworkdayjobs.com/wday/cxs/globalhr/REC_RTX_Ext_Gateway/jobs",
    "NGC": "https://ngc.wd1.myworkdayjobs.com/wday/cxs/ngc/Northrop_Grumman_External_Site/jobs",
    "gm": "https://generalmotors.wd5.myworkdayjobs.com/wday/cxs/generalmotors/Careers_GM/jobs",
    "Autodesk": "https://autodesk.wd1.myworkdayjobs.com/wday/cxs/autodesk/Ext/jobs",
    "adobe": "https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/external_experienced/jobs",
    "Capital One": "https://capitalone.wd12.myworkdayjobs.com/wday/cxs/capitalone/Capital_One/jobs",
    "Paypal": "https://paypal.wd1.myworkdayjobs.com/wday/cxs/paypal/jobs/jobs",
    "Fidelity": "https://wd1.myworkdaysite.com/wday/cxs/fmr/FidelityCareers/jobs", 
    "Vanguard": "https://vanguard.wd5.myworkdayjobs.com/wday/cxs/vanguard/vanguard_external/jobs",
    "Blackrock": "https://blackrock.wd1.myworkdayjobs.com/wday/cxs/blackrock/BlackRock_Professional/jobs",
    "Disney": "https://disney.wd5.myworkdayjobs.com/wday/cxs/disney/disneycareer/jobs",
    "Workday": "https://workday.wd5.myworkdayjobs.com/wday/cxs/workday/Workday/jobs",
    "Warner bros": "https://warnerbros.wd5.myworkdayjobs.com/wday/cxs/warnerbros/global/jobs",
    "Activision": "https://activision.wd1.myworkdayjobs.com/wday/cxs/activision/External/jobs",
    "Sony": "https://sonyglobal.wd1.myworkdayjobs.com/wday/cxs/sonyglobal/SonyGlobalCareers/jobs",
    "Blue Origin": "https://blueorigin.wd5.myworkdayjobs.com/wday/cxs/blueorigin/BlueOrigin/jobs",
    "Shell": "https://shell.wd3.myworkdayjobs.com/wday/cxs/shell/ShellCareers/jobs",
    "Chevron": "https://chevron.wd5.myworkdayjobs.com/wday/cxs/chevron/jobs/jobs",
    "Genentech": "https://roche.wd3.myworkdayjobs.com/wday/cxs/roche/ROG-A2O-GENE/jobs"
}

seen = set()
def create_job(company: str, role: str, location: str, date_posted: str, link: str, days: int,  db):
    if db.get(models.Job, link): return
    job = models.Job(Company = company, Role = role, Location = location, Date_Posted = date_posted, Link = link, Days = days)
    db.add(job)



if __name__ == "__main__":
    models.Base.metadata.create_all(bind = engine)

    db = SessionLocal()

    session = requests.Session()
    session.headers.update(headers)

    try:
        for k,v in workday_companies.items():
            for page in range(0, 100, 20):
                payload["offset"] = page

                for attempt in range(3):
                    try:
                        response = session.post(v, json= payload, timeout = (3,5))
                        break
                    except (ConnectionError, Timeout):
                        time.sleep(2)
                else: continue

                if response.status_code != 200:
                    break

                result = response.json()
                for job in result["jobPostings"]:
                    
                    role = job.get("title", "N/A")
                    if "intern" not in role.lower(): continue

                    location = (job.get("locationsText", "N/A"))

                    postedOn = job.get("postedOn", "N/A")

                    link = job.get("externalPath", "N/A")
                    base= v.split("/wday/cxs/", 1)[0]
                    rest = v.split("/wday/cxs/",1)[1]
                    other = rest.split("/", 2)[1]
                    final_link = (f"{base}/en-US/{other}{link}")
                    days = (0 if postedOn == "Posted Today" else 1 if postedOn == "Posted Yesterday" else int(''.join(filter(str.isdigit, postedOn))))
                    if final_link in seen: continue
                    seen.add(final_link)
                    create_job(k, role,location,postedOn,final_link, days, db)

                    
                
                time.sleep(.3)
        jobs = db.query(models.Job).filter(models.Job.Days >= 30).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()