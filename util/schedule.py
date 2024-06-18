"""
定时事件逻辑处理
"""

from threading import Timer
from loguru import logger
from bilibili_api import sync
from lib import live
from util import config

def schedule_ctrl(setmin:int,arg:str,settype: int):
    sec=setmin*60
    if settype == 1:
        logger.debug(str(min)+"min "+str(arg))       
        Timer(sec,schedule_run,args=[arg,sec]).setDaemon(True)
        Timer(sec,schedule_run,args=[arg,sec]).start()
    if settype == 2:
        Timer(sec,schedule_run,args=[arg,sec]).cancel()

def schedule_run(text:str,sec:int):
    logger.debug(str(sec)+text)
    try:
        sync(live.LIVEROOM.send_danmaku(danmaku=live.Danmaku(text=text)))
    except:
        logger.warning("schedule error!")
    finally:
        Timer(sec,schedule_run,args=[text,sec]).setDaemon(True)
        Timer(sec,schedule_run,args=[text,sec]).start()
    return

def close():
    try:
        cfg = config.roomcfg['chat']['global']['schedule']
    except TypeError:
        return
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']),2)
    return

def create_schedule():
    try:
        cfg = config.roomcfg['chat']['global']['schedule']
    except TypeError:
        return
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']),1)
    return
