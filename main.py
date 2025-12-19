import requests, gspread, time, os
from google.oauth2.service_account import Credentials
from requests.exceptions import ConnectionError
from dotenv import load_dotenv

load_dotenv("key.env")
scope_key = os.getenv("scope_key")
sheet_id = os.getenv("sheet_id")

scopes = [
    scope_key
]
creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)

sheet_id = sheet_id
sheet = client.open_by_key(sheet_id).sheet1



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

apps = []
session = requests.Session()
session.headers.update(headers)


for k,v in workday_companies.items():
    for page in range(0, 100, 20):
        payload["offset"] = page

        try:
            response = session.post(v, json= payload, timeout = 10)
        except ConnectionError:
            time.sleep(2)
            continue

        if response.status_code != 200:
            break

        result = response.json()
        for job in result["jobPostings"]:
            role = job.get("title", "N/A")
            if "intern" not in role.lower(): continue
            
            location = job.get("locationsText", "N/A")


            postedOn = job.get("postedOn", "N/A")
            link = job.get("externalPath", "N/A")
            base= v.split("/wday/cxs/", 1)[0]
            rest = v.split("/wday/cxs/",1)[1]
            other = rest.split("/", 2)[1]
            link = f"{base}/en-US/{other}{link}"
            value = 0 if postedOn == "Posted Today" else 1 if postedOn == "Posted Yesterday" else int(''.join(filter(str.isdigit, postedOn)))
            apps.append(list((k,role, location, postedOn, link, value)))
        
        time.sleep(.3)


rows = sheet.get_all_values()
header = rows[0]
filter = [
    row for row in apps
    if "30" not in row[3]
]

sheet.clear()
sheet.update([["Company", "Role", "Location", "Posted On", "Link", "Days Since"], *filter])
sheet.sort((6,  "asc"))