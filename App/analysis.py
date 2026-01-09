import pandas as pd
import matplotlib as plt
from .database import engine

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

    "SWE_BACKEND": [
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

    "SWE_FRONTEND": [
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

    "IT": [
        "%it support%", "%help desk%", "%helpdesk%",
        "%desktop support%", "%service desk%",
        "%system administrator%", "%sysadmin%",
        "%network administrator%",
        "%active directory%", "%windows server%",
        "%o365%", "%azure ad%", "%vmware%"
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
    "EMBEDDED_ROBOTICS": [
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
    df[k] = pd.read_sql('SELECT "Company", "Role" FROM "Jobs" WHERE "Role" ILIKE ANY (%s)', conn, params = (v,))

for topic, frame in df.items():
    print("\n\n",topic)
    print(frame)