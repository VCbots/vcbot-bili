import random
import json
from time import sleep
from loguru import logger
from bilibili_api import Credential,Danmaku,sync
from bilibili_api.live import LiveDanmaku,LiveRoom

def set(room:int,credential:Credential):
    global LiveDanma
    LiveDanma = LiveDanmaku(room_display_id=room,credential=credential)
    global liveroom
    liveroom = LiveRoom(room_display_id=room,credential=credential)
    get_room_owner_uid()
    return

async def send_danmu(text: str = None):
    lens=len(text)
    logger.debug(lens)
    if lens > 20:
        for i in range(0,lens,20):
            text_splited=text[i:i+20]
            logger.info(f'send:{text_splited}')
            try:
                sleep(random.random()+0.2) #预防api返回 10030（您发送弹幕的频率过快）
                await liveroom.send_danmaku(danmaku=Danmaku(text=text_splited))
            except UnboundLocalError as e:
                logger.warning(str(e))
            except BaseException as e:
                logger.warning(str(e))
                return
    else:    
        logger.info(f'send:{text}')
        try:
            sleep(random.random()+0.3) #预防api返回 10030（您发送弹幕的频率过快）
            await liveroom.send_danmaku(danmaku=Danmaku(text=text))
        except UnboundLocalError as e:
            logger.warning(str(e))
        except BaseException as e:
                logger.warning(str(e))
                return

            
def get_room_owner_uid():
    i = sync(liveroom.get_room_info())
    global owner_uid
    owner_uid = str(i['room_info']['uid'])
    return owner_uid