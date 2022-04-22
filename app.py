import websocket, json, pprint
import vonage
import config
import pandas as pd
import EMA 
import heikin_ashi as ha
import stoch_rsi as srsi
from termcolor import colored
from binance.client import Client
from binance.enums import *




closes = []
opens= []
highs= []
lows= []
playon=False

SOCKET = "wss://stream.binance.com:9443/ws/dotusdt@kline_1m"
#vonage client for sending SMS, key and secret
clientel = vonage.Client(config.V_KEY, config.V_SECRET)
sms = vonage.Sms(clientel)

# binance clients keys and secret
client = Client(config.API_KEY, config.API_SECRET)

#percentage to cash out
margin_percentage = config.margin_percentage

#Trading Setup

pair,round_off = ["DOTUSDT"], [5]

def sendsms(messagestring):
    responseData = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": "2348136410056",
        "text": "Second text message from peauli",
    }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


def buy(symbol,quoteOrderQty):
    try:
        print("sending order")
        #order = client.order_market_buy(symbol=symbol, quoteOrderQty=quoteOrderQty)
        order=client.create_test_order(symbol=symbol,side="BUY", type="MARKET",quoteOrderQty=quoteOrderQty)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

def sell( symbol,quoteOrderQty):
    try:
        print("sending order")
        #order = client.order_market_sell(symbol=symbol, quoteOrderQty=quoteOrderQty)
        order=client.create_test_order(symbol=symbol,side="SELL", type="MARKET",quoteOrderQty=quoteOrderQty)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, playon
    

    #print('received message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message["k"]

    is_candle_closed = candle['x']
    close = candle['c']
    open = candle['o']
    low = candle['l']
    high = candle['h']
    
    if is_candle_closed:      
        closes.append(float(close))
        opens.append(float(open))
        lows.append(float(low))
        highs.append(float(high))
        pprint.pprint(json_message)

        print(opens,end=" ")
        print(highs,end=" ")
        print(lows,end=" ")
        print(closes)
        if len(closes) > 1:

            current_open = opens[-1]
            current_close = closes[-1]
            current_high = highs[-1]
            current_low = lows[-1]
            previous_open = opens[-2]
            previous_close = closes[-2]


            Oprice,Hprice,Lprice,Cprice= ha.HEIKIN(current_open,current_high,current_low,current_close,previous_open,previous_close)
            print("HEIKIN ASHI")
            print(Oprice,end=" ")
            print(Hprice,end=" ")
            print(Lprice,end=" ")
            print(Cprice)



            firstsource=EMA.ema(Cprice,3)
            if len(firstsource > 3):
                emasource=EMA.ema(firstsource,3)
                stochsource=pd.DataFrame(emasource, columns=['close'])
                print(stochsource)
                rsi,stoch_k,stoch_d = srsi.stoch_rsi_tradingview(stochsource)
        

                print("stoch_k and stoch_d")
                print(stoch_k)
                print(stoch_d)
                print(stoch_k.iat[-1])
                print(stoch_d.iat[-1])
        
        
        

                my_quote_asset = config.quote
                my_round_off = round_off[0]

                # Retrieve Current Asset INFO
                asset_info      = client.get_symbol_ticker(symbol=pair[0])
                asset_price     = float(asset_info.get("price"))
                order_price  = asset_price
                asset_balance   = float(client.get_asset_balance(asset="DOT").get("free"))

                # Computing for Trade Quantity
                current_holding = round(asset_balance * asset_price, my_round_off)
                order_holding   = current_holding
                change_percent  = round(((asset_price - order_price) / order_price * 100), my_round_off)
                takeprofit= round((current_holding - order_holding), my_round_off)

        
                # Output Console and Placing Order
         
                if playon:
                    if (abs(change_percent) > margin_percentage):
                        sell(symbol=pair[0], quoteOrderQty=takeprofit)
                        order_holding =round(asset_balance * asset_price, my_round_off)
                        order_price=asset_price
                        playon=True
                        sendsms("I just took a profit of "+ " " + str(takeprofit) )

                    elif (stoch_k.iat[-1] < stoch_d.iat[-1]) or (Cprice[-1] < Oprice[-1]):
                        sell(symbol=pair[0], quoteOrderQty=current_holding)
                        playon=False
                        sendsms("I just sold all your asset")
                
                    else:
                        sendsms("It is overbought, but we don't own any. Nothing to do")
                        

                elif (stoch_k.iat[-1] > stoch_d.iat[-1]): 
                    if playon:
                        sendsms("It is oversold, but you already own it, nothing to do.")
                    else:

                        buy(symbol=pair[0], quoteOrderQty=current_holding)
                        order_holding =round(asset_balance * asset_price, my_round_off)
                        order_price = asset_price
                        playon=True
                        sendsms("We just entered an uptrend and i have bought some asset")
                

                else:
                    sendsms("Nothing to do now waitng for the right time")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()










