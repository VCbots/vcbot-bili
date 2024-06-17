from bilibili_api import Credential,Danmaku
from bilibili_api.live import LiveDanmaku,LiveRoom

def room_set(room:int,credential:Credential):
    global LiveDanma
    LiveDanma = LiveDanmaku(room_display_id=room,credential=credential)
    global liveroom
    liveroom = LiveRoom(room_display_id=room,credential=credential)
    return
