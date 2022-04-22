# Real time_Binance Trading Bot with SMS notification @peauli

This is a trading bot that trades on Binance SPOT WALLET

A Trading Bot that uses a combined Stochastic RSI(StochRSI) and Multi EMA to buy low and sell high.



<a name="hello_disclaimer"></a>
## DISCLAIMER
I have no responsibility for any loss or hardship incurred directly or indirectly by using this code.

PLEASE MANAGE YOUR RISK LEVEL BEFORE USING MY SCRIPT.

USE IT AT YOUR OWN RISK!

<a name="how_it_works"></a>
## HOW-IT-WORKS

**NOTE** For example, for BTCUSDT, BTC is the base asset, USDT is the quote asset.

1. This script implements a strategy that helps you make some profit daily when the market moves up in a cycle and reinvest it in the next cycle.

2. Assuming you have a spot balance of 100 USDT in your Spot wallet and you want to trade BTC

3. When you run the script, the program will automatically purchase BTC using 100 USDT from your `SPOT WALLET` given that our algorithm signals a buy.

4. Whenever the bot make a profit of 0.3% in a 1 minute timeframe, it automatically sells it and starts watching for another 0.3% profit.

5. It closes the position fully when K < D or the last candle is on a downtrend

6.Whenever it take an action, an SMS notification is sent to your phone.

7. The idea is to make some profit daily and accummulating over time.

8. It's more profitable in higher time-frames like 4h,1d etc

7. for more info, your can send an email @preciousajorgba@gmail.com
