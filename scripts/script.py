from pybit.unified_trading import HTTP
from pybit._http_manager import FailedRequestError
import logging
from dotenv import load_dotenv
import os, json, threading
import pandas as pd
import ta
import ta.trend

logging.basicConfig(level=logging.INFO, filename='logs/log_trade.csv', filemode='a', format='%(asctime)s, %(levelname)s, %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
dotenv_path = os.path.join('config', '.env')
load_dotenv(dotenv_path=dotenv_path)

def get_api_keys() -> list:     
    API_KEY = os.getenv("API_KEY")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    accountType = os.getenv("ACCOUNT_TYPE")
    return [API_KEY, API_KEY_SECRET, accountType]

client = HTTP(testnet=False, api_key=get_api_keys()[0], api_secret=get_api_keys()[1])

logging.addLevelName(25, 'BUY')
logging.addLevelName(26, 'SELL')

def loggingBuy(self, message, *args, **kws):
    self._log(25, message, args, **kws)

def loggingSell(self, message, *args, **kws):
    self._log(26, message, args, **kws)

logging.Logger.buy = loggingBuy
logging.Logger.sell = loggingSell

logger = logging.getLogger(__name__)



def place_buy_order(symbol, amount):
    try:
        order = client.place_order(
            category='spot',
            symbol=symbol,
            side='Buy',
            orderType='Market',
            qty=amount,
        )
    except FailedRequestError as e:
        logging.error(e)
        return f"ErrorCode: {e.status_code}"

def place_sell_order(symbol, amount):
    try:
        order = client.place_order(
            category='spot',
            symbol=symbol,
            side='Sell',
            orderType='Market',
            qty=amount
        )
    except FailedRequestError as e:
        logging.error(e)
        return f"ErrorCode: {e.status_code}"

def get_balance():
    try:
        balance = client.get_wallet_balance(accountType=get_api_keys()[2])
        firstCoin, firstCoinName = balance['result']['list'][0]['coin'][0]['walletBalance'], balance['result']['list'][0]['coin'][0]['coin']
        secondCoin, secondCoinName = balance['result']['list'][0]['coin'][1]['walletBalance'], balance['result']['list'][0]['coin'][1]['coin']
        return [firstCoin, firstCoinName, secondCoin, secondCoinName]
    except FailedRequestError as e:
        logging.error(e)
        return f"ErrorCode: {e.status_code}"

def get_kline(interval):
    try:
        kline = client.get_kline(symbol='SOLUSDT', interval=interval)
        return kline
    except FailedRequestError as e:
        logging.error(e)
        return f"ErrorCode: {e.status_code}"
    
def get_kline_dataframe(interval):
    dataframe = pd.DataFrame(get_kline(interval=interval)['result']['list'])
    dataframe.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    dataframe.set_index('time', inplace=True)
    dataframe.index = pd.to_numeric(dataframe.index, downcast='integer').astype('datetime64[ms]')    
    dataframe = dataframe[::-1]
    return dataframe 

def get_bot_config():
    with open(os.path.join('config', 'bot_cfg.json'), 'r') as bot_data_read:
        data = json.load(bot_data_read)
        return data
    

def macd_diff_strategy():
    open_position = False
    
    symbol = get_bot_config()['symbol']
    interval = get_bot_config()['interval']
    amountBuy = get_bot_config()['amountBuy']
    logging.info(f"script macd_diff was started! settings: {symbol}, {interval}, {amountBuy}, 0")

    if open_position: logger.info('activate mode: sell')
    else: logger.info('activate mode: buy')

    while True:        
        df = get_kline_dataframe(interval)
        # logger.info(f'kline dataframe')
        if not open_position:
            if ta.trend.macd_diff(df.close).iloc[-1] > 0 \
            and ta.trend.macd_diff(df.close).iloc[-2] < 0:
                place_buy_order(symbol, amountBuy)
                logger.buy(f'opened position in {symbol} for {amountBuy} USDT')
                open_position = True
                       
        if open_position:
            if ta.trend.macd_diff(df.close).iloc[-1] < 0 \
            and ta.trend.macd_diff(df.close).iloc[-2] > 0:
                amountSell = get_balance()[0][:5]
                place_sell_order(symbol, amountSell)
                logger.sell(f'close position in {symbol} for {amountSell} USDT')
                open_position = False



def SMA_strategy():
    open_position = False
    
    symbol = get_bot_config()['symbol']
    interval = get_bot_config()['interval']
    amountBuy = get_bot_config()['amountBuy']
    logging.info(f"script sma_strategy was started! settings: {symbol}, {interval}, {amountBuy}, 0")

    if open_position: logger.info('activate mode: sell')
    else: logger.info('activate mode: buy') 
    while True:        
        df = get_kline_dataframe(interval)
        sma_short = ta.trend.sma_indicator(df.close, window=9)
        sma_long = ta.trend.sma_indicator(df.close, window=21)
        if not open_position:
            if sma_short.iloc[-1] > sma_long.iloc[-1] \
            and sma_short.iloc[-2] < sma_long.iloc[-2]:
                place_buy_order(symbol, amountBuy)
                logger.buy(f'opened position in {symbol} for {amountBuy} USDT')
                open_position = True
                       
        if open_position:
            if sma_short.iloc[-1] < sma_long.iloc[-1] \
            and sma_short.iloc[-2] > sma_long.iloc[-2]:
                amountSell = get_balance()[0][:5]
                place_sell_order(symbol, amountSell)
                logger.sell(f'close position in {symbol} for {amountSell} USDT')
                open_position = False

if __name__ == '__main__':
    SMA_strategy()


