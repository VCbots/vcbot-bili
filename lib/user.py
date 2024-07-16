from bilibili_api import Credential,login,user,sync

def user_login():
    import tkinter as tk
    a = login.login_with_qrcode(tk.Tk())
    return a

def user_login_term():
    a = login.login_with_qrcode_term()
    return a

async def user_info(uid:int,Credential: Credential):
    u = user.User(uid=uid,credential=Credential)
    info = await u.get_user_info()
    return info

def get_self_uid(Credential: Credential):
    i= sync( user.get_self_info(credential=Credential))
    global bot_uid
    bot_uid=str(i['mid'])
    print(bot_uid)
    return bot_uid

