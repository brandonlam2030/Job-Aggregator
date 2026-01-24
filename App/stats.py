import pandas as pd
import matplotlib.pyplot as plt
from .database import engine
import numpy as np

conn = engine.connect()
subcategories = {
    "ML/AI": [
        "%machine learning%", "%ml%", "%ai%", "%artificial intelligence%",
        "%deep learning%", "%neural%", "%nlp%", "%speech recognition%",
        "%computer vision%", "%vision language%", "%multimodal%",
        "%reinforcement learning%", "%rl%",
        "%world model%", "%agent%", "%agentic%",
        "%foundation model%", "%large language model%", "%llm%",
        "%model alignment%", "%model scaling%",
        "%applied research%", "%research scientist%",
        "%mlops%", "%ml infrastructure%",
        "%data scientist%", "%data science%",
        "%drug discovery%", "%computational biology%", "%bioinformatics%"
    ],

    "SWE_Backend": [
        "%software engineer%", "%software engineering%",
        "%backend%", "%server%", "%api%",
        "%systems%", "%system software%",
        "%distributed%", "%platform%",
        "%infrastructure%", "%cloud%",
        "%devops%", "%ci/cd%",
        "%cuda%", "%gpu software%",
        "%compiler%", "%llvm%",
        "%performance%", "%profiling%",
        "%test development%", "%validation%",
        "%storage%", "%filesystem%"
    ],

    "SWE_Frontend": [
        "%frontend%", "%front end%",
        "%full stack%", "%full-stack%",
        "%ui%", "%ux%",
        "%visualization%", "%hci%",
        "%web%", "%dashboard%",
        "%design and development%"
    ],

    "Cybersecurity": [
        "%cybersecurity%", "%security engineer%", "%security analyst%",
        "%application security%", "%appsec%",
        "%cloud security%", "%iam%",
        "%threat detection%", "%incident response%",
        "%siem%", "%soc%", "%penetration testing%", "%pentest%",
        "%vulnerability%", "%zero trust%"
    ],
    "Hardware": [
        "%hardware%", "%asic%", "%soc%",
        "%vlsi%", "%rtl%",
        "%verification%", "%dft%",
        "%physical design%", "%floorplan%",
        "%validation%", "%bring-up%",
        "%circuit%", "%analog%", "%mixed-signal%",
        "%photonic%", "%photonics%",
        "%ic design%", "%chip%",
        "%computer architecture%", "%microarchitecture%",
        "%serdes%"
    ],

    "Product Management": [
        "%product manager%", "%product management%",
        "%technical product manager%", "%tpm%",
        "%roadmap%", "%product strategy%",
        "%requirements%", "%prd%",
        "%stakeholders%", "%go-to-market%"
    ],
    "Embedded Robotics": [
        "%embedded%", "%firmware%",
        "%robot%", "%robotics%",
        "%autonomous%", "%autonomous driving%",
        "%av%", "%vehicle%",
        "%simulation%", "%digital twin%",
        "%real-time%", "%control%",
        "%sensor%", "%lidar%",
        "%embedded software%"
    ]
}



df = {}

for k,v in subcategories.items():
    df[k] = pd.read_sql('SELECT "Company", "Role", "Date_Found"  FROM "Jobs" WHERE "Role" ILIKE ANY (%s)', conn, params = (v,)).set_index("Date_Found")


x = df["ML/AI"].groupby(level = "Date_Found", sort = True).nunique().index
graph_data = pd.DataFrame()

for group in df:
    counts = pd.Series(df[group].index).value_counts().sort_index(ascending = True)
    counts = counts.reindex(x, fill_value = 0)
    cum_counts = counts.cumsum()
    graph_data[group] = cum_counts


percentages = graph_data.pct_change()
percentages.dropna(inplace = True)
print("\n\nNumber of Openings per Day:\n", graph_data.to_string())
print("\n\nPercent Growth in Opportunity:\n", percentages.to_string())


plt.subplot(1,2,1)
plt.plot(percentages)
plt.xlabel("Dates")
plt.ylabel("Percent Growth in Respective Fields")
plt.legend(list(subcategories.keys()))
plt.ylim(0, .3)


plt.subplot(1,2,2)
plt.plot(graph_data)
plt.xlabel("Dates")
plt.ylabel("Number of Openings")
plt.legend(list(subcategories.keys()))

plt.show()

