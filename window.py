import dearpygui.dearpygui as dpg
import json, os
from callbacks.callbacks import *
from windows import settings, bot_settings
from scripts import script


dpg.create_context()


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
                    dpg.add_text(f'balance: {script.get_balance()} | ', tag='balance_tag', parent='main_window_child')
                    dpg.add_button(label="activate")
                    dpg.add_button(label="stop")

            with dpg.child_window(tag='logs_frame_tag'):
                dpg.add_text("logs will be here")



dpg.create_viewport(title='Ihorium', width=1300, height=700, resizable=False)
dpg.setup_dearpygui()
dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()