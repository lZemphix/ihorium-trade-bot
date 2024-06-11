import dearpygui.dearpygui as dpg

def bot_settings_window():
    with dpg.window(label="Bot settings", pos=[400,250], width=400, height=300):
        dpg.add_combo(label="<- currency pair", items=['BTC-USDT', 'ETH-USDT'], default_value='BTC-USDT', tag='currency_tag')
        dpg.add_input_float(label="<- amount (USDT)", tag="ammount_tag", min_value=0, min_clamped=True)


