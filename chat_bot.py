from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config

my_token = config('TELEGRAM_TOKEN')

updater = Updater(my_token, use_context=True)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    if callback_header != "" :
        text_header += ","

    for text in text_list :
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list

def get_command(update, context):
    print("get")
    show_list = []
    show_list.append(InlineKeyboardButton("on", callback_data="on")) # add on button
    show_list.append(InlineKeyboardButton("off", callback_data="off")) # add off button
    show_list.append(InlineKeyboardButton("cancel", callback_data="cancel")) # add cancel button
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

    update.message.reply_text("원하는 값을 선택하세요", reply_markup=show_markup)

def callback_get(update, context) :
    data_selected = update.callback_query.data
    print("callback : ", data_selected)
    if data_selected.find("cancel") != -1 :
        context.bot.edit_message_text(text="취소하였습니다.",
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)
        return

    if len(data_selected.split(",")) == 1 :
        button_list = build_button(["1", "2", "3", "cancel"], data_selected)
        show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
        context.bot.edit_message_text(text="상태를 선택해 주세요.",
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=show_markup)

    elif len(data_selected.split(",")) == 2 :
        context.bot.edit_message_text(text="{}이(가) 선택되었습니다".format(update.callback_query.data),
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)
get_handler = CommandHandler('get', get_command)
updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))

updater.dispatcher.add_handler(get_handler)

updater.start_polling(timeout=1, clean=True)
updater.idle()