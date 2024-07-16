import os
import json
from lib import user,live,config,content,ignore,schedule
from loguru import logger
from bilibili_api import Credential,sync


def login():
    global c
    logger.info('Try to login from cookie.json...')
    try:
        cook=json.load(open(file=f"./cookie.json"))
        c = Credential(sessdata=cook["SESSDATA"],bili_jct=cook["bili_jct"],buvid3=cook["buvid3"],ac_time_value=cook["ac_time_value"],dedeuserid=cook["DedeUserID"])
    except:
        logger.info('Failed!Please login with qrcode!')
        if config.term_env == '1':
            c = user.user_login_term()
        elif config.term_env is None:
            c = user.user_login()
        try:
            c.raise_for_no_sessdata()
            c.raise_for_no_bili_jct()
            coco=json.dumps(c.get_cookies(),ensure_ascii=False)
        except:
            logger.exception("Login error!")
            os._exit(1)
        finally:
            with open(file="./cookie.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
                cookies.write(coco)
    user.get_self_uid(c)
    logger.info('Login successfully!')


        
def main():     
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        # 连接成功
        logger.info('Connected!')
        await live.send_danmu(text=config.roomcfg["connected"])
        logger.debug(event)
    
    @live.LiveDanma.on('GUARD_BUY')
    async def on_guard(event):
        # 上舰长/提督/总督
        logger.debug(json.dumps(event,ensure_ascii=False))
        text=content.get_danmaku_on_buyguard(event=event)
        await live.send_danmu(text=text)



    @live.LiveDanma.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕.
        text=""
        if event['data']['info'][2][0] == user.bot_uid:
            return
        try:
            text=content.get_danmaku_content(event=event)
        except UnboundLocalError as e:
            logger.warning(str(e))
            return
            
        if text == "":
            return 
        
        await live.send_danmu(text=text)



    @live.LiveDanma.on('INTERACT_WORD')
    async def on_welcome(event):
        # 用户进入直播间/关注
        text=""
        if event['data']['data']['is_spread'] == 1:
            logger.debug(json.dumps(event,ensure_ascii=False))
            logger.info('spread is true,ignore.')
            return
        uid=str(event['data']['data']['uid'] ) 
        if ignore.check_ban_inital(uid=uid) == True:
            logger.info('uid_ban is true,ignore.')
            return 
        if str(uid) == live.owner_uid:
            logger.info('The uid is room owner,ignore.')
            return 
        
        types=event['data']['data']['msg_type'] #判断是关注还是进入
        if types == 1:
            text=content.get_danmaku_on_wuser(event=event)
        if types == 2:
            text=content.get_danmaku_on_user_followed(event=event)
        if text == "":
            return
        await live.send_danmu(text=text)



        logger.debug(json.dumps(event,ensure_ascii=False))

    @live.LiveDanma.on('SEND_GIFT')
    async def on_gift(event):
        # 收到礼物
        
        logger.debug(json.dumps(event,ensure_ascii=False))
        text = content.get_danmaku_on_gift(event=event)


    skip_schedule = False
    try:
        logger.info('Loading schedule...')
        schedule.start()
    except:
        skip_schedule=True
        logger.warning('schedule not set,skiped.')
    try:
        logger.info('Connecting to the liveroom...')
        sync(live.LiveDanma.connect())
    except:
        #正常关闭
        print("\n")
        logger.info("Closing...")
        if skip_schedule == False:
            schedule.close()
        sync(live.LiveDanma.disconnect())
        os._exit(0)

if __name__ == "__main__" :
    config.loadroomcfg()
    logger.info(config.roomcfg)
    login()
    live.set(room=config.room,credential=c)
    main()

