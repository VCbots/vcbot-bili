import tkinter as tk
from bilibili_api import Credential,login,user

def user_login():
    a = login.login_with_qrcode(tk.Tk())
    return a

async def user_info(uid:int,Credential: Credential):
    u = user.User(uid=uid,credential=Credential)
    info = await u.get_user_info()
    return info

