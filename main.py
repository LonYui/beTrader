import websocket
from web3 import Web3
import json,time
from dydx3 import Client

以太地址 = '0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a'.lower()
# 2/10 從網頁拿的資料
api鑰匙 = {"0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a":{"walletAddress":"0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a","secret":"-oh0a7mJPFGOQJJiB8xAtdDcanhDdO0r9ZGvS8QE","key":"85d657e2-93bc-c88f-57a4-38ad6a2dff3e","passphrase":"ZqZGgqVYXsFn2dZy7WRF","legacySigning":False,"walletType":"METAMASK"}}
STARK鑰匙 = {"0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a":{"walletAddress":"0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a","publicKey":"06511d93334ad2fd8d1923e63305d22f76826c8f4efcae13d9b3a93ee28595c4","publicKeyYCoordinate":"02f75e050183b6fe37eec4be825cf1068a4b993b93599ddb3451cb42ee077fee","privateKey":"03d8a60dc0de6fc58bf787e922018792362418fba7e173dc567d1a5c2cfb732a","legacySigning":False,"walletType":"METAMASK"}}

客戶端 = Client(host = "https://api.stage.dydx.exchange",
             # api_key_credentials={'key':api鑰匙['0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a'][],
             #                      'secret':'',
             #                      'passphrase':''},
             api_key_credentials=api鑰匙['0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a'],
             stark_private_key=STARK鑰匙['0x1C9D9fB55779499F0ebCf700ac4b6EC183DD7b2a']['privateKey'],
             default_ethereum_address=以太地址,
             network_id='5',
)

測試請求的回覆 = 客戶端.private.get_account()
position_id = 測試請求的回覆.data['account']['positionId']

def 掛單():
    # 參數 = {'position_id':position_id,
    #       'market':'ETH-USD',
    #       'side':'BUY',
    #       'order_type':'LIMIT',
    #       'post_only':True,
    #       'size':'0.01',
    #        'price':'1500',
    #       'limit_fee':'0.0015',
    #       'expiration_epoch_seconds':time.time() + 2*60*1000}
    參數 = {'position_id': position_id, 'market': 'ETH-USD', 'side': 'BUY',
                    'order_type': 'LIMIT', 'post_only': True, 'size': '0.01',
                    'price': '1500', 'limit_fee': '0.0015',
                    'expiration_epoch_seconds': time.time() + 24*60*60}
    response = 客戶端.private.create_order(**參數)


def 取得掛單資料(市場):

    def 開始前(ws):
        print('start')
        channel_data = {"type":"subscribe","channel":"v3_orderbook","id":市場,"includeOffsets":True}
        # channel_data = {"type": "subscribe", "channel": "v3_orderbook", "id": str(security_name),"includeOffsets": "True"}
        # ws.send(json.dump(channel_data))
        ws.send(json.dumps(channel_data))
    def 進行中(ws,msg):
        print(msg)
    def 結束後(ws):
        print('結束了唷')

    socket = "wss://api.stage.dydx.exchange/v3/ws"
    # socket = "wss://api.stage.dydx.exchange/v3/ws"
    # ws = websocket.WebSocketApp(socket,on_open=開始前,on_message=進行中,on_close=結束後)
    ws = websocket.WebSocketApp(socket, on_open=開始前, on_message=進行中, on_close=結束後)

    ws.run_forever()


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')