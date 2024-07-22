from loguru import logger
from .libs import config

def get_danmaku_content(event:str):
    uid=event["data"]["info"][2][0]
    content=event["data"]["info"][1]
    logger.info(content)
    try:
        contents=config.roomcfg["chat"][f"{uid}"]["command"][content]
    except:
        try:
            contents=config.roomcfg["chat"]["global"]["command"][content]
            logger.info("Reply:"+str(contents))
        except KeyError as e:
            return ""
    return contents

def get_danmaku_on_gift(event:str):
    info = event['data']['data']
    giftname=info['giftName']
    name= info['uname']
    try:
        contents=str(config.plugins_cfg['gift']['message'])
        content_name=contents.replace(" {user} ",f"{name}")
        contented=content_name.replace(" {gift} ",f"{giftname}")
    except:
        logger.info("Reply:"+str(contented))
    return contented

def get_danmaku_on_wuser(event:str):
    info = event['data']['data']
    name= info['uname']
    try:
        contents=str(config.plugins_cfg['welcome']['message'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        logger.info("reply:"+str(content_name))
    return content_name

def get_danmaku_on_buyguard(event:str):
    info = event['data']['data']
    print(info)
    giftname=info['gift_name']
    name= info['username']
    num= info['num']
    try:
        contents=str(config.plugins_cfg['guard']['message'])
        content_name=contents.replace(" {user} ",f"{name}")
        content_num=content_name.replace(" {type} ",f"{giftname}")
        contented=content_num.replace(" {num} ",f"{num}")
    except:
        logger.info("Reply:"+str(contented))
    return contented

def get_danmaku_on_user_followed(event:str):
    print(event)
    info = event['data']['data']
    name= info['uname']
    try:
        contents=str(config.plugins_cfg['followed']['message'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        logger.info("reply:"+str(content_name))
    return content_name

def _get_guard_type(num:int):
    if num == 1:
        return "总督"
    if num == 2:
        return "提督"
    if num == 3:
        return "舰长"
    