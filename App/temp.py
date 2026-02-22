import requests, time
from datetime import datetime, timezone
from requests.exceptions import ConnectionError, Timeout
import pandas as pd
from pathlib import Path

#temp.py is a parquet uploader in situations where PostgreSQL DB quota is at limit

headers = {"Content-Type": "application/json"}
payload = {
    
    "appliedFacets":{"employmentType":["Internship"]},
    "limit":20,
    "offset":0,
    "searchText": "",
    "totalSelectedFacetsCount": 0
}

workday_companies = {
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
    "GM": "https://generalmotors.wd5.myworkdayjobs.com/wday/cxs/generalmotors/Careers_GM/jobs",
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
    "Genentech": "https://roche.wd3.myworkdayjobs.com/wday/cxs/roche/ROG-A2O-GENE/jobs",
    "Labcorp": "https://labcorp.wd1.myworkdayjobs.com/wday/cxs/labcorp/External/jobs",
    "Aveva": "https://aveva.wd3.myworkdayjobs.com/wday/cxs/aveva/AVEVA_careers/jobs",
    "Athena Health": "https://athenahealth.wd1.myworkdayjobs.com/wday/cxs/athenahealth/External/jobs",
    "UPS": "https://hcmportal.wd5.myworkdayjobs.com/wday/cxs/hcmportal/Search/jobs",
    "Samsung": "https://sec.wd3.myworkdayjobs.com/wday/cxs/sec/Samsung_Careers/jobs",
    "Dexcom": "https://dexcom.wd1.myworkdayjobs.com/wday/cxs/dexcom/Dexcom/jobs",
    "Walmart": "https://walmart.wd5.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs",
    "Ribbon": "https://vhr-genband.wd1.myworkdayjobs.com/wday/cxs/vhr_genband/ribboncareers/jobs",
    "Aerospace Company": "https://aero.wd5.myworkdayjobs.com/wday/cxs/aero/External/jobs",
    "PWC": "https://pwc.wd3.myworkdayjobs.com/wday/cxs/pwc/Global_Experienced_Careers/jobs"
}
terms = [
    "machine learning", "ml", "ai", "artificial intelligence",
    "deep learning", "neural", "nlp", "speech recognition",
    "computer vision", "vision language", "multimodal",
    "reinforcement learning", "rl",
    "world model", "agent", "agentic",
    "foundation model", "large language model", "llm",
    "model alignment", "model scaling",
    "applied research", "research scientist",
    "mlops", "ml infrastructure",
    "data scientist", "data science",
    "drug discovery", "computational biology", "bioinformatics",

    "software engineer", "software engineering",
    "backend", "server", "api",
    "systems", "system software",
    "distributed", "platform",
    "infrastructure", "cloud",
    "devops", "ci/cd",
    "cuda", "gpu software",
    "compiler", "llvm",
    "performance", "profiling",
    "test development", "validation",
    "storage", "filesystem",

    "frontend", "front end",
    "full stack", "full-stack",
    "ui", "ux",
    "visualization", "hci",
    "web", "dashboard",
    "design and development",

    "cybersecurity", "security engineer", "security analyst",
    "application security", "appsec",
    "cloud security", "iam",
    "threat detection", "incident response",
    "siem", "soc", "penetration testing", "pentest",
    "vulnerability", "zero trust",

    "hardware", "asic", "soc",
    "vlsi", "rtl",
    "verification", "dft",
    "physical design", "floorplan",
    "bring-up",
    "circuit", "analog", "mixed-signal",
    "photonic", "photonics",
    "ic design", "chip",
    "computer architecture", "microarchitecture",
    "serdes",

    "product manager", "product management",
    "technical product manager", "tpm",
    "roadmap", "product strategy",
    "requirements", "prd",
    "stakeholders", "go-to-market",

    "embedded", "firmware",
    "robot", "robotics",
    "autonomous", "autonomous driving",
    "av", "vehicle",
    "simulation", "digital twin",
    "real-time", "control",
    "sensor", "lidar",
    "embedded software"
]
interns = [
    "intern",
    "internship",
    "co-op",
    "coop",
    "co operative",
    "student",
    "summer",
    "graduate intern"
]



jobs = []


if __name__ == "__main__":

    session = requests.Session()
    session.headers.update(headers)

    try:
        print("enter")
        date = datetime.now(timezone.utc)
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
                if not result.get("jobPostings"): break
                for job in result["jobPostings"]:
                    
                    role = job.get("title", "N/A").lower()
                    if not any(intern in role for intern in interns): continue

                    if any(term in role for term in terms):
                        location = (job.get("locationsText", "N/A"))
                        link = job.get("externalPath", "N/A")
                        base= v.split("/wday/cxs/", 1)[0]
                        rest = v.split("/wday/cxs/",1)[1]
                        other = rest.split("/", 2)[1]
                        final_link = (f"{base}/en-US/{other}{link}")
                        jobs.append({
                            "Company": k,
                            "Role": role,
                            "Date_Found": date,
                            "Location": location,
                            "Link": final_link
                        })


                    
                
                time.sleep(.3)
    except Exception as e:
        print("fail", repr(e))
    finally:
        print("done")
        df = pd.DataFrame(jobs)
        out = Path("buffer/jobs.parquet")
        out.parent.mkdir(parents=True,exist_ok = True)
        df = df.drop_duplicates(subset = ["Company", "Role", "Link"])
        if df.empty: 
            print("No jobs found")
            exit(0)
        if out.exists() and out.stat().st_size > 0:
            old = pd.read_parquet(out)
            df = pd.concat([old,df], ignore_index = True)
        df.to_parquet(out,index=False)
