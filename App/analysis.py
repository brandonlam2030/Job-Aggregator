from docx import Document
from pathlib import Path
import pandas as pd
from . import models
from .database import engine, SessionLocal
from sqlalchemy.dialects.postgresql import insert



db = SessionLocal()
def extract(file):
    doc = Document(file)

    string = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    job = insert(models.Resume).values(Content = string)
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
finally: 
    db.close()