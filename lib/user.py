"""
user
"""

import tkinter as tk
from bilibili_api import Credential,login,user
bot_uid = None

def user_login():
    a = login.login_with_qrcode(tk.Tk())
    return a

async def user_info(uid:int,User_credential: Credential):
    u = user.User(uid=uid,credential=User_credential)
    info = await u.get_user_info()
    return info

async def get_self_uid(User_Credential: Credential):
    i= await user.get_self_info(credential=User_Credential)
    global bot_uid
    bot_uid=i['mid']
    return bot_uid
