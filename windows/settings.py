from callbacks.callbacks import *
from windows import about


def settings_window():
    dpg.delete_item('settings_window_tag')
    with dpg.window(label="Settings", pos=[400,250], width=450, height=300, tag=f'settings_window_tag'):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_settings) 
        with dpg.child_window():
            dpg.add_combo(label="<- Theme (soon)", items=['dark', 'light'], default_value=open_app_config()['theme'], tag='theme_tag')
            dpg.add_button(label="About", callback=about.about_window)