import os
import json
import datetime
from loguru import logger
from bilibili_api import Credential,sync
from plugins.libs import user,live,config
from plugins import content,ignore,schedule,at,blind

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
        if config.plugins_cfg['connected']['enable'] is True:
            await live.send_danmu(text=config.plugins_cfg["connected"]['message'])
        logger.debug(event)
    
    @live.LiveDanma.on('GUARD_BUY')
    async def on_guard(event):
        # 上舰长/提督/总督
        logger.debug(json.dumps(event,ensure_ascii=False))
        if config.plugins_cfg['guard']['enable'] is True:
            text=content.get_danmaku_on_buyguard(event=event)
        await live.send_danmu(text=text)



    @live.LiveDanma.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕.
        text=""
        
        if str(event['data']['info'][2][0]) == user.bot_uid:
            #这里不写log，防止刷日志
            return
        
        if at.check_at(event=event) is True:
            await at.send_at_notice(event=event)
            logger.info('The danmaku has @user,reminded.')
            return
        

        try:
            text=content.get_danmaku_content(event=event)
        except BaseException as e:
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
        if types == 1 and config.plugins_cfg['welcome']['enable'] is True:
            text=content.get_danmaku_on_wuser(event=event)
        if types == 2 and config.plugins_cfg['followed']['enable'] is True:
            text=content.get_danmaku_on_user_followed(event=event)
        if text == "":
            return
        await live.send_danmu(text=text)
        logger.debug(json.dumps(event,ensure_ascii=False))

    @live.LiveDanma.on('SEND_GIFT')
    async def on_gift(event):
        # 收到礼物
        logger.debug(json.dumps(event,ensure_ascii=False))
        if config.plugins_cfg['gifts']['enable'] is False:
            return
        if event['data']['data']['blind_gift'] != None and config.plugins_cfg['blind']['enable'] is True:
            await blind.on_blind(event=event)
            logger.info('The gift was blind gift,it will replace.')
            return
        text = content.get_danmaku_on_gift(event=event)
        await live.send_danmu(text=text)
        


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

def start():
    today=datetime.date.today()
    logger.add(f'./logs/log-{str(today)}.log',format='{time} {level} {function} - {message}')
    logger.info('Starting...')
    config.loadroomcfg()
    login()
    live.set(room=config.room,credential=c)
    main()

if __name__ == "__main__" :
    start()