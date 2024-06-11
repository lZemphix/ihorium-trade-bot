from pybit.unified_trading import HTTP
from pybit._http_manager import FailedRequestError, InvalidRequestError, JSONDecodeError
import logging
from dotenv import load_dotenv
import os


dotenv_path = os.path.join('config', '.env')
load_dotenv(dotenv_path=dotenv_path)
    
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
accountType = os.getenv("ACCOUNT_TYPE")

client = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_KEY_SECRET
)
logging.basicConfig(level=logging.INFO, filename='log.txt', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


def get_balance():
    try:
        balance = client.get_wallet_balance(accountType=accountType)
        return f"{balance['result']['list'][0]['coin'][0]['walletBalance']} {balance['result']['list'][0]['coin'][0]['coin']}"
    except FailedRequestError as e:
        if e.status_code == 401:
            logging.error(e.status_code + e.message)    
            return 'ErrorCode: 401'
    except Exception as e:
        logging.error(e)
        print(e)
