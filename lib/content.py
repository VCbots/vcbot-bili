from . import user
from loguru import logger
import main

def get_danmaku_content(event:str):
    uid=event["data"]["info"][2][0]
    content=event["data"]["info"][1]
    logger.info(content)
    try:
        contents=main.config.roomcfg["chat"][f"{uid}"]["command"][content]
    except:
        try:
            contents=main.config.roomcfg["chat"]["global"]["command"][content]
            logger.info("Reply:"+str(contents))
        except KeyError as e:
            return ""
    return contents

def get_danmaku_on_gift(event:str):
    info = event['data']['data']
    giftname=info['giftName']
    name= info['uname']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['gifts'])
        content_name=contents.replace(" {user} ",f"{name}")
        contented=content_name.replace(" {gift} ",f"{giftname}")
    except:
        logger.info("Reply:"+str(contented))
    return contented

def get_danmaku_on_wuser(event:str):
    info = event['data']['data']
    name= info['uname']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['welcome'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        logger.info("reply:"+str(content_name))
    return content_name

def get_danmaku_on_buyguard(event:str):
    info = event['data']
    print(info)
    giftname=get_guard_type(int(info["guard_level"]))
    name= info['username']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['guard'])
        content_name=contents.replace(" {user} ",f"{name}")
        contented=content_name.replace(" {type} ",f"{giftname}")
    except:
        logger.info("Reply:"+str(contented))
    return contented

def get_danmaku_on_user_followed(event:str):
    print(event)
    info = event['data']['data']
    name= info['uname']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['followed'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        logger.info("reply:"+str(content_name))
    return content_name

def get_guard_type(num:int):
    if num == 1:
        return "总督"
    if num == 2:
        return "提督"
    if num == 3:
        return "舰长"
    