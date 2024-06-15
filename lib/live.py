from bilibili_api import Credential,live,Danmaku
from bilibili_api.live import LiveDanmaku,LiveRoom

def set(room:int,credential:Credential):
    global LiveDanma
    LiveDanma = LiveDanmaku(room_display_id=room,credential=credential)
    global liveroom
    liveroom = LiveRoom(room_display_id=room,credential=credential)
    return
