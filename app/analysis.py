import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests, time
from bs4 import BeautifulSoup
import duckdb
from .extract import headers, clean
from requests.exceptions import RequestException


#analysis.py is a lightweight NLP that optimizes resumes for certain jobs

con = duckdb.connect("jobs.duckDB")


links = con.execute("SELECT * FROM jobs;").df()["Link"]
final = []
text = []
for link in links:
    temp = link.split("/")
    company = temp[2].split(".")[0]
    final.append(temp[0] + "//" + temp[2] + "/wday/cxs/" + company + "/" + temp[4] + "/" + temp[5] + "/" + temp[6] + "/" + temp[7])

c=0
for link in final:
    for attempt in range(3):
        try:
            resp = requests.get(link, headers= headers, timeout = 10)

            if resp.status_code != 200:
                c+=1
                break
            
            try:
                res = resp.json()
            except: 
                break
            
            if "jobPostingInfo" not in res:
                break
            words = BeautifulSoup(res["jobPostingInfo"]["jobDescription"], "html.parser").get_text(strip = True, separator = " ")
            text.append(clean(words))
            break
        except RequestException: time.sleep(2)

resumes = con.execute("SELECT * FROM resumes").df()["Normalized"]
tfidf = TfidfVectorizer(stop_words = "english", min_df = 2, max_df =.85, ngram_range = (1,2))

corpus = resumes.to_list() + text
result = tfidf.fit_transform(corpus)
x = result[:len(resumes.to_list())]
y = result[len(resumes.to_list()):]


similarities = cosine_similarity(x,y)
print(similarities)
