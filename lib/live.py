"""
live
"""
from bilibili_api import Credential,Danmaku
from bilibili_api.live import LiveDanmaku,LiveRoom

LIVEROOM = None
LIVEDANMA = None

def room_set(room:int,credential:Credential):
    """
    init liveroom
    """
    global LIVEROOM
    global LIVEDANMA
    LIVEDANMA = LiveDanmaku(room_display_id=room,credential=credential)
    LIVEROOM = LiveRoom(room_display_id=room,credential=credential)
