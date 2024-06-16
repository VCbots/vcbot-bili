import tkinter as tk
from bilibili_api import Credential,login,user

def user_login():
    a = login.login_with_qrcode(tk.Tk())
    return a

async def user_info(uid:int,Credential: Credential):
    u = user.User(uid=uid,credential=Credential)
    info = await u.get_user_info()
    return info

async def get_self_uid(Credential: Credential):
    i= await user.get_self_info(credential=Credential)
    global bot_uid
    bot_uid=i['mid']
    return bot_uid
