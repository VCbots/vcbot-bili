from . import user
import main

def get_danmaku_content(event:str):
    uid=event["data"]["info"][2][0]
    content=event["data"]["info"][1]
    print(content)
    #print(name["name"],content)
    try:
        contents=main.config.roomcfg["chat"][f"{uid}"]["command"][content]
    except:
        print(contents)
    return contents

def get_danmaku_ongift(event:str):
    info = event['data']['data']
    uid = info['uid']
    giftname=info['giftName']
    name= info['sender_uinfo']['base']['name']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['gifts'])
        contented=contents.replace(" {user} ",f"{name}")
    except:
        print(contented)
        raise

    return contented