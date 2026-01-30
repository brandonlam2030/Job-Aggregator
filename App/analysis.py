from docx import Document
from pathlib import Path
import pandas as pd
from . import models
from .database import engine, SessionLocal
from sqlalchemy.dialects.postgresql import insert
from sklearn.feature_extraction.text import TfidfVectorizer
import re, string, requests, time

headers = {
    "Content-Type": "application/json"
}


# db = SessionLocal()
# models.Base.metadata.create_all(bind = engine)

skills = {
    r"machine.learning": "machine learning",
    r"c\+\+": "cpp",
    r"node[\. ]?js": "nodejs",
    r"\bsoftware[\.\-\s]?engineer(ing)?\b": "software engineer",
    r"\bhtml\d*\b":"html",
    r"angular[\. ]?js":"angularjs",
    r"\bcss\d*\b":"css",
    r"\b(postgresql|mysql|mariadb|sqlite|sql\s*server)\b": "sql",
    r"c#":"csharp"



}

# def extract(file):
#     doc = Document(file)

#     temp = "\n".join(p.text.lower() for p in doc.paragraphs if p.text.strip())


#     normal = str.maketrans("","", string.punctuation)
#     s = temp.translate(normal)

#     s = re.sub(r"\d", "", s)
#     s = re.sub(" +", " ", s)
    
#     for k,v in skills.items():
#         s = re.sub(k,v,s)
    

#     if temp and s:
#         job = insert(models.Resume).values(Content = temp, Normalized = s)
#         db.execute(job)

#     return 



# directory_path = Path("archive/Resumes")
# for person in directory_path.iterdir():

#     extract(person)

# try: 
#     db.commit()
# except Exception as e: 
#     print("fail", repr(e))
#     db.rollback()






# resumes = [
#     r.Normalized
#     for r in db.query(models.Resume).all()
#     if r.Normalized and r.Normalized.strip()
# ]
# tfidf = TfidfVectorizer(stop_words = "english", min_df = 2, max_df =.85, ngram_range = (1,2))
# result = tfidf.fit_transform(resumes)
# terms = tfidf.get_feature_names_out()


# links = pd.Series(db.query(models.Job.Link).all())
# print(links)


initial = ["https://autodesk.wd1.myworkdayjobs.com/en-US/Ext/job/Toronto-ON-CAN/Intern--Construction-UX-Research_25WD94406-1"]
final = []
for link in initial:
    temp = link.split("/")
    company = temp[2].split(".")[0]
    final.append(temp[0] + "//" + temp[2] + "/wday/cxs/" + company + "/" + temp[4] + "/" + temp[5] + "/" + temp[6] + "/" + temp[7])


for attempt in range(3):
    try:
        resp = requests.get(final[0], headers= headers, timeout = 10)
        res = resp.json()
        break
    except: time.sleep(2)
print(res["jobPostingInfo"])

