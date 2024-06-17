"""
程序主入口
"""

import os
import json
from loguru import logger
from bilibili_api import Credential,sync
from lib import user,live
from util import config,content,ignore,schedule


def login():
    """
    登录
    """

    try:
        cook=json.load(open(file="./cookie.json"))
        global c
        c = Credential(
            sessdata=cook["SESSDATA"],
            bili_jct=cook["bili_jct"],buvid3=cook["buvid3"],
            ac_time_value=cook["ac_time_value"],
            dedeuserid=cook["DedeUserID"]
        )
    except:
        logger.info('Can not get Credential,please login with qrcode!')
        c = user.user_login()
        try:
            c.raise_for_no_sessdata()
            c.raise_for_no_bili_jct()
            coco=json.dumps(c.get_cookies(),ensure_ascii=False)
        except:
            logger.exception("Login error!Now exiting...")
            os._exit(1)
        finally:
            logger.info("Login successfully!Now will wrote the Credential to cookie.json...")
            with open(file="./cookie.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
                cookies.write(coco)
    finally:
        logger.info('Login successfully!Now starting...')
    return

def main():
    @live.LiveDanma.on('VERIFICATION_SUCCESSFUL')
    async def on_successful(event):
        # 连接成功
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=config.roomcfg["connected"]))
        except:
            logger.info("connect command not found!")
        logger.info("Connect successfully!")
        logger.info('Start successfully!')
        logger.debug(event)

    @live.LiveDanma.on('GUARD_BUY')
    async def on_guard(event):
        # 上舰长/提督/总督
        logger.debug(json.dumps(event,ensure_ascii=False))
        text=content.get_danmaku_on_buyguard(event=event)
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except UnboundLocalError as e:
            logger.warning(str(e))


    @live.LiveDanma.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕.
        text=""
        await user.get_self_uid(Credential=c)
        if event['data']['info'][2][0] is user.bot_uid:
            return
        try:
            text=content.get_danmaku_content(event=event)
        except UnboundLocalError as e:
            logger.warning(str(e))
            return

        if text == "":
            return 

        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except UnboundLocalError as e:
            logger.warning(str(e))


    @live.LiveDanma.on('INTERACT_WORD')
    async def on_welcome(event):
        # 用户进入直播间/关注
        text=""
        if event['data']['data']['is_spread'] == 1:
            logger.debug(json.dumps(event,ensure_ascii=False))
            logger.info('spread is true,ignore.')
            return
        uid=str(event['data']['data']['uid'])
        if ignore.check_ban_inital(uid=uid) is True:
            logger.info('uid_ban is true,ignore.')
            return
        types=event['data']['data']['msg_type'] #判断是关注还是进入
        if types == 1:
            text=content.get_danmaku_on_wuser(event=event)
        if types == 2:
            text=content.get_danmaku_on_user_followed(event=event)
        if text == "":
            return
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except UnboundLocalError as e:
            logger.warning(str(e))
        except Exception as e:
            logger.warning(str(e))


        logger.debug(json.dumps(event,ensure_ascii=False))

    @live.LiveDanma.on('SEND_GIFT')
    async def on_gift(event):
        # 收到礼物
        logger.debug(json.dumps(event,ensure_ascii=False))
        text = content.get_danmaku_on_gift(event=event)
        try:
            await live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text))
        except UnboundLocalError as e:
            logger.warning(str(e))

    skip_schedule = False
    try:
        schedule.main()
    except:
        skip_schedule=True
        logger.warning('schedule not set,skiped.')
    try:
        sync(live.LiveDanma.connect())
    except:
        #正常关闭
        print("\n")
        logger.info("Closing...")
        if skip_schedule is False:
            schedule.close()
        sync(live.LiveDanma.disconnect())
        logger.info("close successfully!")
        os._exit(0)

if __name__ == "__main__" :
    config.loadroomcfg()
    logger.info(config.roomcfg)
    login()
    live.set(room=config.room,credential=c)
    main()
