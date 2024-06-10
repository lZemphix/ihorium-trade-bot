import dearpygui.dearpygui as dpg
import json, os
from callback.callbacks import *


dpg.create_context()

with dpg.window(label="main window", width=1, height=1, no_resize=True) as main_window:
    with dpg.group(horizontal=True):
        dpg.add_button(label="settings", callback=settings_window)
    with dpg.child_window():
        pass


dpg.create_viewport(title='Ihorium', width=1300, height=700, resizable=False)
dpg.setup_dearpygui()
dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()