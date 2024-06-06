import os
import sys
import json
from lib import user,live,config,content
from bilibili_api import Credential,sync

def login():
    global c
    try:
        cook=json.load(open(file=f"./cookie.json"))
        c = Credential(sessdata=cook["SESSDATA"],bili_jct=cook["bili_jct"],buvid3=cook["buvid3"],ac_time_value=cook["ac_time_value"],dedeuserid=cook["DedeUserID"])
    except:
        c = user.user_login()
        try:
            c.raise_for_no_sessdata()
            c.raise_for_no_bili_jct()
            coco=json.dumps(c.get_cookies(),ensure_ascii=False)
        except:
            print("error!")
        finally:
            with open(file="./cookie.json",mode="w",encoding="utf-8") as cookies:
                cookies.write(coco)


def main():     
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=config.roomcfg["connected"]))
        print(event)
    
    @live.LiveDanma.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕.
        Uid=event["data"]["info"][2][0]
        print(Uid)
        contents=event["data"]["info"][1]
        try:
            text=content.get_danmaku_content(event=event)
            print(text)
        except: #如果user不存在命令，走global
            try:
                text=config.roomcfg["chat"]["global"]["command"][contents]
                print(text)
            except KeyError:
                print("\n")
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except:
            print("\n")

        name=await user.user_info(uid=Uid,Credential=c)
        print(json.dumps(event,ensure_ascii=False))
        print(name["name"],event["data"]["info"][1])


    @live.LiveDanma.on('SEND_GIFT')
    async def on_gift(event):
        # 收到礼物,todo
        print(json.dumps(event,ensure_ascii=False))
    
    sync(live.LiveDanma.connect())

if __name__ == "__main__" :
    config.loadroomcfg()
    print(config.roomcfg)
    login()
    live.set(room=config.room,credential=c)
    main()

