import dearpygui.dearpygui as dpg
import json, os, pathlib
from dotenv import load_dotenv, set_key
from scripts import script

dotenv_path = pathlib.Path('config/.env')
load_dotenv(dotenv_path=dotenv_path)

def balance_widget(user_data):  
    dpg.delete_item('balance_tag')
    dpg.add_text(f'balance: {user_data}', tag='balance_tag', parent='main_window_child')



def save_config():
    set_key(dotenv_path, 'API_KEY', dpg.get_value('api_token'))
    set_key(dotenv_path, 'API_KEY_SECRET', dpg.get_value('api_secret_token'))
    set_key(dotenv_path, 'ACCOUNT_TYPE', dpg.get_value('account_type'))
    dpg.set_value('balance_tag', value=f'balance: {script.get_balance()}')
    dpg.delete_item('settings_window_tag')
    



def settings_window():
    dpg.delete_item('settings_window_tag')
    path = os.path.join('config', '.env')
    if os.path.isfile(path):
        API_KEY = os.getenv("API_KEY")
        API_KEY_SECRET = os.getenv("API_KEY_SECRET")
        accountType = os.getenv("ACCOUNT_TYPE")

    with dpg.window(label="Settings", pos=[400,250], width=450, height=300, tag=f'settings_window_tag'):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_config) 
        with dpg.child_window():
            dpg.add_input_text(label="<- API key", tag="api_token", password=True, default_value=API_KEY)
            dpg.add_input_text(label="<- API secret key", tag="api_secret_token", password=True, default_value=API_KEY_SECRET)
            # dpg.add_input_text(label="<- Account type", tag="account_type", default_value=accountType)
            dpg.add_combo(label="<- Account type", items=['CONTRACT', 'UNIFIED'], default_value=accountType, tag='account_type')
