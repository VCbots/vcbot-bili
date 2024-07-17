def check_ban_inital(uid:str):
    #黑名单，遇到以下uid直接忽略
    if uid == '3546377875360540':
        return True
    if uid == '3546632014531086':
        return True
    return False