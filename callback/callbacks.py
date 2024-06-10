import dearpygui.dearpygui as dpg
import json, os, pathlib
from dotenv import load_dotenv, set_key

dotenv_path = pathlib.Path('config/.env')
load_dotenv(dotenv_path=dotenv_path)

def save_config():
    set_key(dotenv_path, 'API_KEY', dpg.get_value('api_token'))
    set_key(dotenv_path, 'API_KEY_SECRET', dpg.get_value('api_secret_token'))
    dpg.delete_item('settings_window_tag')

def settings_window():
    dpg.delete_item('settings_window_tag')
    path = os.path.join('config', '.env')
    if os.path.isfile(path):
        API_KEY = os.getenv("API_KEY")
        API_KEY_SECRET = os.getenv("API_KEY_SECRET")
        print(API_KEY, API_KEY_SECRET)

    with dpg.window(label="Settings", pos=[400,250], width=450, height=300, tag=f'settings_window_tag'):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_config) 
        with dpg.child_window():
            dpg.add_input_text(label="<- API key", tag="api_token", password=True, default_value=API_KEY)
            dpg.add_input_text(label="<- API secret key", tag="api_secret_token", password=True, default_value=API_KEY_SECRET)

if __name__ == '__main__':
    pass