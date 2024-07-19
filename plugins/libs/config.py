import os
import json
from loguru import logger
from dotenv import load_dotenv

default={'connected': '连接成功!', 'chat': {'global': {'schedule': [{'minute': 30, 'content': '主包记得喝水！'}, {'minute': 15, 'content': '关注上舰送灯牌，寻找主包不迷路～'}], 'events': {'reply_notice': ' {user} 回复 {re-user} : {content} ', 'welcome': '欢迎 {user} 进入直播间', 'gifts': '谢谢 {user} 的 {gift} 喵～', 'guard': '感谢 {user} 开通 {type} 喵～', 'followed': '感谢 {user} 的关注喵～'}, 'command': {'about-rule': 'default rule v1.0', 'about': 'vcbot-bili v0.1.3 Made by@luyanci'}}, '282873551': {'command': {'debug': 'vcbot-bili with default rule'}}}}

def loadroomcfg():
    load_dotenv(dotenv_path="./.env")
    global room
    room=os.environ["roomid"]
    global term_env
    term_env = os.environ["term_env"]
    global roomcfg
    try:
        roomcfg = json.load(open(f"./{room}.json",encoding="utf-8",errors="ignore"))
    except:
        roomcfg = default
        _make_default_cfg()
    finally:
        logger.info(str(roomcfg))
    return

def _make_default_cfg():
    with open(file=f"./{room}.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
        cookies.write(json.dumps(default,ensure_ascii=False))