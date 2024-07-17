import random
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
            await _send_it(text=text_splited)
    else:    
        await _send_it(text=text)

            
def get_room_owner_uid():
    i = sync(liveroom.get_room_info())
    global owner_uid
    owner_uid = str(i['room_info']['uid'])
    return owner_uid

async def _send_it(text:str):
    failed=False
    sleep(random.random()+0.2)  #预防api返回 10030/10031（您发送弹幕的频率过快)
    try:
        await liveroom.send_danmaku(danmaku=Danmaku(text=text))
    except BaseException as e:
        failed = True
        logger.warning(f'send failed:{e}')
        if str(e).find('您发送弹幕的频率过快',0) != -1 or str(e) == 'Server disconnected': #过分了（弹幕发送过快/断开连接-->1s后重新发送）
            logger.warning(f'Trying to resend({text}) in 1-2s...')
            sleep(1+random.random()) 
            await _send_it(text=text)
    finally:
        if failed is False:
            logger.info(f'sended:{text}')
