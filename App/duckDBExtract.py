import duckdb
import os
from dotenv import load_dotenv

#duckDBExtract.py pulls all PostgreSQL DB data into a DuckDB local DB

load_dotenv("key.env")
con = duckdb.connect("jobs.duckdb")

con.execute("INSTALL postgres_scanner;")
con.execute("LOAD postgres_scanner;")
con.execute(f"ATTACH '{os.getenv("RAW_CONNECTION_URL")}' AS JA (TYPE POSTGRES);")
# con.execute("CREATE TABLE jobs AS SELECT * FROM JA.Jobs;")
#  con.execute("CREATE TABLE resumes AS SELECT * FROM JA.Resume")
con.execute("CREATE OR REPLACE TABLE jobs AS SELECT * FROM JA.Jobs;")
con.execute("CREATE OR REPLACE TABLE resumes AS SELECT * FROM JA.Resume;")

print(con.execute("SELECT * FROM resumes LIMIT 10").df())

