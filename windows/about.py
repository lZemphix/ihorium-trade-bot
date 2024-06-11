from callbacks.callbacks import *


def about_window():
    with dpg.texture_registry():
        width, height, channels, data = dpg.load_image("src/logo.png")
        texture_id = dpg.add_static_texture(width, height, data)
    with dpg.window(label="About", pos=[400,250], width=450, height=300, tag='about_window_tag'):        
        dpg.add_image(texture_id)
        dpg.add_text(f"""
version: {os.getenv('PROJECT_VERSION')}
author: {os.getenv('PROJECT_CREATORS')}""")