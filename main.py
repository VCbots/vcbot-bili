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
            with open(file="./cookie.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
                cookies.write(coco)


def main():     
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        # 连接成功
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=config.roomcfg["connected"]))
        except:
            print("connect command not found!")
        print(event)
    
    @live.LiveDanma.on('GUARD_BUY')
    async def on_guard(event):
        # 上舰长/提督/总督
        print(json.dumps(event,ensure_ascii=False))
        text=content.get_danmaku_on_buyguard(event=event)
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except:
            print(" ")
        print(json.dumps(event,ensure_ascii=False))

    @live.LiveDanma.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕.
        try:
            text=content.get_danmaku_content(event=event)
        except:
            print(" ")
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except:
            print(" ")

    @live.LiveDanma.on('INTERACT_WORD')
    async def on_welcome(event):
        # 用户进入直播间/关注
        types=event['data']['data']['msg_type'] #判断是关注还是进入
        if types == 1:
            text=content.get_danmaku_on_wuser(event=event)
        if types == 2:
            text=content.get_danmaku_on_user_followed(event=event)
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except:
            print(" ")

        print(json.dumps(event,ensure_ascii=False))

    @live.LiveDanma.on('SEND_GIFT')
    async def on_gift(event):
        # 收到礼物
        print(json.dumps(event,ensure_ascii=False))
        text = content.get_danmaku_on_gift(event=event)
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except:
            print(" ")

    sync(live.LiveDanma.connect())

if __name__ == "__main__" :

    config.loadroomcfg()
    print(config.roomcfg)
    login()
    live.set(room=config.room,credential=c)
    main()

