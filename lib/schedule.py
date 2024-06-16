from . import config,live
from loguru import logger
from threading import Timer
from bilibili_api import sync

def schedule_ctrl(min:int,arg:str,type: int):
    sec=min*60
    if type == 1:
        logger.debug(str(min)+"min "+str(arg))       
        Timer(sec,schedule_run,args=[arg]).setDaemon(True)
        Timer(sec,schedule_run,args=[arg]).start()
    if type == 2:
        Timer(sec,schedule_run,args=[arg]).cancel()
    return

def schedule_run(text:str):
    try:
        sync(live.liveroom.send_danmaku(danmaku=live.Danmaku(text=text)))
    except:
        logger.warning("schedule error!")
    return

def close():
    cfg = config.roomcfg['chat']['global']['schedule']
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']),2)
    return

def main():
    cfg = config.roomcfg['chat']['global']['schedule']
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']),1)
    return