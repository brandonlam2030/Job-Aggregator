import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import requests, time
from bs4 import BeautifulSoup
from .extract import headers, clean
from . import models
from .database import engine, SessionLocal

#analysis.py is a lightweight NLP that optimizes resumes for certain jobs

db = SessionLocal()
models.Base.metadata.create_all(bind = engine)

resumes = [
    r.Normalized
    for r in db.query(models.Resume).all()
    if r.Normalized and r.Normalized.strip()
]
tfidf = TfidfVectorizer(stop_words = "english", min_df = 2, max_df =.85, ngram_range = (1,2))
result = tfidf.fit_transform(resumes)
terms = tfidf.get_feature_names_out()


# links = pd.Series(db.query(models.Job.Link).all())



initial = ["https://autodesk.wd1.myworkdayjobs.com/en-US/Ext/job/Toronto-ON-CAN/Intern--Construction-UX-Research_25WD94406-1"]
final = []
text = []
for link in initial:
    temp = link.split("/")
    company = temp[2].split(".")[0]
    final.append(temp[0] + "//" + temp[2] + "/wday/cxs/" + company + "/" + temp[4] + "/" + temp[5] + "/" + temp[6] + "/" + temp[7])


for link in final:
    for attempt in range(3):
        try:
            resp = requests.get(link, headers= headers, timeout = 10)
            res = resp.json()
            words = BeautifulSoup(res["jobPostingInfo"]["jobDescription"], "html.parser").get_text(strip = True, separator = " ")
            text.append(clean(words))
            break
        except: time.sleep(2)

series = pd.Series(text)
tfidf = TfidfVectorizer(stop_words = "english", min_df = 0.0, max_df =1, ngram_range = (1,2))
print(series)
text_result = tfidf.fit_transform(series)
print(text_result)
print(tfidf.get_feature_names_out())
