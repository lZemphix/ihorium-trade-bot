import dearpygui.dearpygui as dpg
import json, os, pathlib
from dotenv import load_dotenv, set_key
from scripts import script


dotenv_path = pathlib.Path('config/.env')
load_dotenv(dotenv_path=dotenv_path)


def get_api_keys():
    if os.path.isfile(os.path.join('config', '.env')):
        API_KEY = os.getenv("API_KEY")
        API_KEY_SECRET = os.getenv("API_KEY_SECRET")
        accountType = os.getenv("ACCOUNT_TYPE")
        return API_KEY, API_KEY_SECRET, accountType
    
def open_app_config():
    with open(os.path.join('config', 'app_cfg.json'), 'r') as settings_data:
        data = json.load(settings_data)
        return data

def save_settings():
    data = open_app_config()
    data['theme'] = dpg.get_value('theme_tag')
    with open('config/app_cfg.json', 'w') as file:
        json.dump(data, file, indent=4)

def save_config():
    set_key(dotenv_path, 'API_KEY', dpg.get_value('api_token'))
    set_key(dotenv_path, 'API_KEY_SECRET', dpg.get_value('api_secret_token'))
    set_key(dotenv_path, 'ACCOUNT_TYPE', dpg.get_value('account_type'))

    with open(os.path.join('config', 'bot_cfg.json'), 'r') as bot_data_read:
        data = json.load(bot_data_read)

    data['symbol'] = dpg.get_value('currency_tag')
    data['amountBuy'] = round(dpg.get_value('ammount_tag'), 4)
    data['amountSell'] = float(script.get_balance()[0])
    with open('config/bot_cfg.json', 'w') as bot_data_write:
        json.dump(data, bot_data_write, indent=4)

    dpg.delete_item('bot_settings_window_tag')
    



