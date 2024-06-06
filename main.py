import os
import sys
import json
from lib import user,live
from bilibili_api import sync
from dotenv import load_dotenv
roomid = "roomid"
def login():
    global c
    c = user.user_login()
    try:
        c.raise_for_no_sessdata()
        c.raise_for_no_bili_jct()
        print()
    except:
        print("error!")

def main():     
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=roomcfg["connected"]))
        print(event)
    
    @live.LiveDanma.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕.
        Uid=event["data"]["info"][2][0]
        name=await user.user_info(uid=Uid,Credential=c)
        print(name["name"],event["data"]["info"][1])


    @live.LiveDanma.on('SEND_GIFT')
    async def on_gift(event):
        # 收到礼物
        print(json.dumps(event,ensure_ascii=False))
    
    sync(live.LiveDanma.connect())

if __name__ == "__main__" :
    load_dotenv(dotenv_path="./.env")
    room=os.environ[roomid]
    global roomcfg
    roomcfg = json.load(open(f"./{room}.json"))
    print(roomcfg)
    login()
    live.set(room=room,credential=c)
    main()

