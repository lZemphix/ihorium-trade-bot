import dearpygui.dearpygui as dpg
import os
from callbacks.callbacks import *

def bot_settings_window():
    dpg.delete_item('bot_settings_window_tag')
    with dpg.window(label="Bot settings", pos=[400,250], width=450, height=300, tag='bot_settings_window_tag'):
        path = os.path.join('config', '.env')
        if os.path.isfile(path):
            API_KEY = os.getenv("API_KEY")
            API_KEY_SECRET = os.getenv("API_KEY_SECRET")
            accountType = os.getenv("ACCOUNT_TYPE")

        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_config) 
        with dpg.child_window():
            dpg.add_input_text(label="<- API key", tag="api_token", password=True, default_value=API_KEY)
            dpg.add_input_text(label="<- API secret key", tag="api_secret_token", password=True, default_value=API_KEY_SECRET)
            dpg.add_combo(label="<- Account type", items=['CONTRACT', 'UNIFIED'], default_value=accountType, tag='account_type') 
            dpg.add_text()   
            dpg.add_combo(label="<- currency pair (only SOL)", items=['SOLUSDT', 'BTHUSDT'], default_value='SOLUSDT', tag='currency_tag')
            dpg.add_input_double(label="<- amount (USDT)", tag="ammount_tag", min_value=3.5, min_clamped=True)


