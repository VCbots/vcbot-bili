import os
import json
from dotenv import load_dotenv

def loadroomcfg():
    load_dotenv(dotenv_path="./.env")
    global room
    room=os.environ["roomid"]
    global term_env
    term_env = os.environ["term_env"]
    print(term_env)
    global roomcfg
    roomcfg = json.load(open(f"./{room}.json",encoding="utf-8",errors="ignore"))
    return