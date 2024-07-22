import os
import json
from loguru import logger
from dotenv import load_dotenv

default={'chat': {'282873551': {'command': {'debug': 'vcbot-bili with default rule'}}, 'global': {'command': {'about': 'vcbot-bili v0.1.3 Made by@luyanci', 'about-rule': 'default rule v1.0'}, 'plugins': {'at': {'enable': True}, 'blind': {'enable': True}, 'connected': {'enable': True, 'message': '连接成功!'}, 'followed': {'enable': True, 'message': '感谢 {user} 的关注喵～'}, 'gifts': {'enable': True, 'message': '谢谢 {user} 的 {gift} 喵～'}, 'guard': {'enable': True, 'message': '感谢 {user} 开通 {type} 喵～'}, 'welcome': {'enable': True, 'message': '欢迎 {user} 进入直播间'}}, 'schedule': [{'content': '主包记得喝水！', 'minute': 30}, {'content': '关注上舰送灯牌，寻找主包不迷路～', 'minute': 15}]}}}

def loadroomcfg():
    load_dotenv(dotenv_path="./.env")
    global room
    room=os.environ["roomid"]
    global term_env
    term_env = os.environ["term_env"]
    global roomcfg
    global plugins_cfg
    try:
        roomcfg = json.load(open(f"./{room}.json",encoding="utf-8",errors="ignore"))
    except:
        roomcfg = default
        _make_default_cfg()
    finally:
        plugins_cfg=roomcfg['chat']['global']['plugins']
        logger.info(str(roomcfg))
    return

def _make_default_cfg():
    with open(file=f"./{room}.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
        cookies.write(json.dumps(default,ensure_ascii=False))
            
if __name__ == "__main__":
    #方便转换，直接运行这个py文件
    roomcfg = json.load(open("example.json",encoding="utf-8",errors="ignore"))
    print(roomcfg)
    with open('dist.txt',encoding='utf-8',errors='ignore',mode='w') as dists:
        dists.write(str(roomcfg))