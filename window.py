import dearpygui.dearpygui as dpg
from callbacks.callbacks import *
from windows import bot_settings, settings
from scripts import script
import pandas as pd, numpy as np
import threading
import logging
import time
import subprocess
dpg.create_context()

logging.basicConfig(level=logging.INFO, filename='logs/log_trade.csv', filemode='a', format='%(asctime)s, %(levelname)s, %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

def cmd_open():
    def op():
        subprocess.run(['E:\python_projects\Ihorium_trader\scripts'])
    threading.Thread(target=op, daemon=True, name='cmd_open').start()

def restart():
    def a():
        subprocess.run(['PowerShell','exit'])
    threading.Thread(target=a, daemon=True, name='cmd_open').start()

def logs():       
    while True:
        time.sleep(1)
        df = pd.read_csv('logs/log_trade.csv', index_col='date')[::-1]
        arr = df.to_numpy()
        dpg.set_value('logs_tag', df)

threading.Thread(target=logs, daemon=True, name='logs').start()


with dpg.window(label="main window", width=1, height=1, no_resize=True, tag='main_window') as main_window:
    with dpg.group(horizontal=True):
        dpg.add_button(label="settings", callback=settings.settings_window)
        dpg.add_button(label="bot settings", callback=bot_settings.bot_settings_window)
    with dpg.group(horizontal=True):
        with dpg.child_window(tag='left_frame_tag', width=170): 
            dpg.add_text("left_frame")

        with dpg.group(horizontal=False):        
            with dpg.child_window(height=35, tag='top_frame_tag'):
                with dpg.group(horizontal=True):
                    fc, fcn, sc, scn = script.get_balance()
                    dpg.add_text(f'balance: {fc} {fcn}, {sc} {scn} | ', tag='balance_tag')
                    dpg.add_button(label="activate", callback=cmd_open)
                    dpg.add_button(label="stop", callback=restart)
            with dpg.child_window(tag='graph_frame_tag', height=400):
                dpg.add_plot(label=script.get_bot_config()['symbol'], height=385, width=-1, tag='plot_tag', )
                
                
                pass
            with dpg.child_window(tag='logs_frame_tag') as logs_frame:
                dpg.add_text('logs', tag='logs_tag')
                
                

# [::-1],tag='logs_tag'
dpg.create_viewport(title='Ihorium', width=1100, height=700, resizable=False)
dpg.setup_dearpygui()
dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()