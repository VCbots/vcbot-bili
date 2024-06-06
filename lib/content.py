from . import user
import main

def get_danmaku_content(event:str):
    uid=event["data"]["info"][2][0]
    #name= user.user_info(uid=uid,Credential=main.c)
    content=event["data"]["info"][1]
    print(content)
    #print(name["name"],content)
    try:
        contents=main.config.roomcfg["chat"][f"{uid}"]["command"][content]
    except:
        print(contents)
    return contents