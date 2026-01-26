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
def extract(file):
    doc = Document(file)

    s = "\n".join(p.text.lower() for p in doc.paragraphs if p.text.strip())

    normal = str.maketrans("","", string.punctuation)
    s = s.translate(normal)

    s = re.sub(r"\d", "", s)
    s = re.sub(" +", " ", s)


    job = insert(models.Resume).values(Content = s)
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
    r.Content
    for r in db.query(models.Resume).all()
    if r.Content and r.Content.strip()
]
tfidf = TfidfVectorizer(stop_words = "english", min_df = 2, max_df =.85, ngram_range = (1,2))
result = tfidf.fit_transform(resumes)
terms = tfidf.get_feature_names_out()




print(terms)


