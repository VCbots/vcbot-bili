from . import user
import main

def get_danmaku_content(event:str):
    uid=event["data"]["info"][2][0]
    content=event["data"]["info"][1]
    print(content)
    try:
        contents=main.config.roomcfg["chat"][f"{uid}"]["command"][content]
    except:
        print(" ")
        try:
            contents=main.config.roomcfg["chat"]["global"]["command"][content]
            print(contents)
        except:
            print(" ")
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
        print(contented)


    return contented

def get_danmaku_on_wuser(event:str):
    info = event['data']['data']
    name= info['uname']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['welcome'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        print(content_name)


    return content_name

def get_danmaku_on_buyguard(event:str):
    info = event['data']
    print(info)
    #giftname=info['gift_name']
    name= info['username']
    try:
        contents=str(main.config.roomcfg["chat"]["global"]["events"]['guard'])
        content_name=contents.replace(" {user} ",f"{name}")
        #contented=content_name.replace(" {gift} ",f"{giftname}")
    except:
        print(content_name)
