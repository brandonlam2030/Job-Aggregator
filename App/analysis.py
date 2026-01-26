from docx import Document
from pathlib import Path
import pandas as pd
from . import models
from .database import engine, SessionLocal
from sqlalchemy.dialects.postgresql import insert
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import string



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

def extract(file):
    doc = Document(file)

    temp = "\n".join(p.text.lower() for p in doc.paragraphs if p.text.strip())


    normal = str.maketrans("","", string.punctuation)
    s = temp.translate(normal)

    s = re.sub(r"\d", "", s)
    s = re.sub(" +", " ", s)
    
    for k,v in skills.items():
        s = re.sub(k,v,s)
    

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






resumes = [
    r.Normalized
    for r in db.query(models.Resume).all()
    if r.Normalized and r.Normalized.strip()
]
tfidf = TfidfVectorizer(stop_words = "english", min_df = 2, max_df =.85, ngram_range = (1,2))
result = tfidf.fit_transform(resumes)
terms = tfidf.get_feature_names_out()



