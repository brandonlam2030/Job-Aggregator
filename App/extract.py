from docx import Document
from pathlib import Path
import string, re
from sqlalchemy.dialects.postgresql import insert
from . import models
from .database import engine, SessionLocal


headers = {
    "Content-Type": "application/json"
}


db = SessionLocal()
models.Base.metadata.create_all(bind = engine)

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

def clean(text:str):
    normal = str.maketrans("","", string.punctuation)
    s = text.translate(normal)

    s = re.sub(r"\d", "", s)
    s = re.sub(" +", " ", s)
    
    for k,v in skills.items():
        s = re.sub(k,v,s)
    return s


def extract(file):
    doc = Document(file)

    temp = "\n".join(p.text.lower() for p in doc.paragraphs if p.text.strip())


    s = clean(temp)
    

    if temp and s:
        job = insert(models.Resume).values(Content = temp, Normalized = s)
        db.execute(job)

    return 



directory_path = Path("archive/Resumes")
for person in directory_path.iterdir():

    extract(person)

try: 
    db.commit()
except Exception as e: 
    print("fail", repr(e))
    db.rollback()






