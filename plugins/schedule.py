from .libs import config,live
from loguru import logger
from threading import Timer
from bilibili_api import sync

def schedule_ctrl(min:int,arg:str,type: int):
    sec=min*60
    if type == 1:
        logger.debug(str(min)+"min "+str(arg))       
        Timer(sec,schedule_run,args=[arg,sec]).setDaemon(True)
        Timer(sec,schedule_run,args=[arg,sec]).start()
    if type == 2:
        Timer(sec,schedule_run,args=[arg,sec]).cancel()
    return

def schedule_run(text:str,sec:int):
    logger.debug(str(sec)+text)
    try:
        sync(live.send_danmu(text=text))
    except:
        logger.warning("schedule error!")
    finally:
        Timer(sec,schedule_run,args=[text,sec]).setDaemon(True)
        Timer(sec,schedule_run,args=[text,sec]).start()
    return

def close():
    try:
        cfg = config.roomcfg['chat']['global']['schedule']
    except:
        return
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']),2)
    return

def start():
    try:
        cfg = config.roomcfg['chat']['global']['schedule']
    except:
        return
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']),1)
    return

