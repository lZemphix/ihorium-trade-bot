import dearpygui.dearpygui as dpg
import json, os
from callbacks.callbacks import *
from scripts import script
import windows
import windows.bot_settings


dpg.create_context()



with dpg.window(label="main window", width=1, height=1, no_resize=True, tag='main_window') as main_window:
    with dpg.group(horizontal=True):
        dpg.add_button(label="settings", callback=settings_window)
        dpg.add_button(label="bot settings", callback=windows.bot_settings.bot_settings_window)
        dpg.add_button(label="activate")
        dpg.add_button(label="stop")
    with dpg.child_window(tag='main_window_child'):         
        balance_widget(script.get_balance())
        

        

dpg.create_viewport(title='Ihorium', width=1300, height=700, resizable=False)
dpg.setup_dearpygui()
dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()