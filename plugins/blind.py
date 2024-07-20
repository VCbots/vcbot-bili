from .libs import live

async def on_blind(event:str):
    blind=event['data']['data']['blind_gift']
    origin_gift=blind['original_gift_name']
    price=int(blind['original_gift_price'])/1000 #int后转成金额
    gift_price=int(blind['gift_tip_price'])/1000 #int后转成金额
    origin_action=blind['gift_action']
    
    gift_name=event['data']['data']['giftName']
    user_name=event['data']['data']['uname']
    action=event["data"]['data']['action']
    num=int(event["data"]['data']['num'])
    totals=(gift_price - price)*num
    
    text1=_check_total(totals)
    final_text=f'{user_name}{origin_action}{gift_name}x{num},{text1}' #懒得写到roomcfg里了
    await live.send_danmu(text=final_text)


def _check_total(total:int):
    if total > 0:
        return f'赚{total:0.1f}元'
    elif total < 0: 
        return f'亏{abs(total):0.1f}元'
    else:
        return ''

