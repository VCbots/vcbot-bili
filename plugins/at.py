import json
from .libs import live,config



def check_at(event:str):
    if config.roomcfg['chat']['global']['plugins']['at']['enable'] is False:
        return False
    extra=event['data']['info'][0][15]['extra']
    jsond=json.loads(extra)
    print(jsond['reply_uname'])
    if str(jsond['reply_uname']) == '' or None:
        return False
    else:
        return True
    
async def send_at_notice(event:str):
    extra=event['data']['info'][0][15]['extra']
    jsond=json.loads(extra)
    uname=event['data']['info'][2][1]
    r_uname=jsond['reply_uname']
    text=event['data']['info'][1]
    contented=f'{uname}:@{r_uname} {text}'
    await live.send_danmu(text=contented)