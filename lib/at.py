import json
from bilibili_api import sync
from . import live,config



def check_at(event:str):
    extra=event['data']['info'][0][15]['extra']
    jsond=json.loads(extra)
    print(jsond['reply_uname'])
    if str(jsond['reply_uname']) == '' or None:
        return False
    else:
        return True
    
async def send_at_notice(event:str):
    model = str(config.roomcfg['chat']['global']['events']['reply_notice'])
    extra=event['data']['info'][0][15]['extra']
    jsond=json.loads(extra)
    uname=event['data']['info'][2][1]
    r_uname=jsond['reply_uname']
    text=event['data']['info'][1]
    content_user=model.replace(' {user} ',f'{uname} ')
    content_ruser=content_user.replace(' {re-user} ',f'@{r_uname} ')
    contented=content_ruser.replace(' {content} ',f'{text}')
    await live.send_danmu(text=contented)