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
    with open(os.path.join('config', 'app_cfg.json'), 'r+') as setting_data:
        data = json.load(setting_data)
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
    dpg.delete_item('settings_window_tag')
    




