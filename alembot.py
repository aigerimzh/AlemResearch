import logging
import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_HTTP_API_TOKEN = '********'

FIRST, SECOND = range(2)

index_file = []

def start(bot, update):
    index_file.clear()
    keyboard = [[InlineKeyboardButton("Category 1", callback_data='category_1'),
                 InlineKeyboardButton("Category 2", callback_data='category_2')],
                [InlineKeyboardButton("Category 3", callback_data='category_3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=update.message.chat_id, text="Please choose:", reply_markup=reply_markup)
    return FIRST


def button(bot, update):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))
    index_file.append(query.data)

def start_location(bot, update):
    query = update.callback_query
    index_file.append(query.data)

    keyboard_location = [[InlineKeyboardButton("Location 1", callback_data='location_1'),
                 InlineKeyboardButton("Location 2", callback_data='location_2')],
                [InlineKeyboardButton("Location 3", callback_data='location_3')]]

    reply_markup_location = InlineKeyboardMarkup(keyboard_location)

    bot.send_message(chat_id=query.message.chat_id, text="Please choose:", reply_markup=reply_markup_location)
    return SECOND
    return ConversationHandler.END

updater = Updater(TELEGRAM_HTTP_API_TOKEN)

def send_me(bot, update):
    query = update.callback_query
    index_file.append(query.data)

    bot.sendMessage(chat_id=query.message.chat_id, text='Send me your message:')

send_me_handler = CommandHandler('send_me', send_me)
updater.dispatcher.add_handler(send_me_handler)

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def save_message(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Пиши и схороню")
    print(index_file)
    print('aaaa')
    saved_text = update.message.text
    print(update.message.from_user.username)
    filename = "Alem/"+index_file[0]+"/"+index_file[1]+"/file-%s.json" %update.message.from_user.username
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, "a+", encoding='utf8')
    # with open(filename, "a+") as f:
    f.write(json.dumps(saved_text, ensure_ascii=False))
    # f.write(saved_text)
    f.write("\n")
    f.close()
    bot.sendMessage(chat_id=update.message.chat_id, text="Есть контакт!")


save_message_handler = MessageHandler(Filters.text, save_message)
updater.dispatcher.add_handler(save_message_handler)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [CallbackQueryHandler(start_location)],
        SECOND: [CallbackQueryHandler(send_me)],
    },
    fallbacks=[CommandHandler('start_location', start_location)]
)
updater.dispatcher.add_handler(conv_handler)

updater.start_polling()

updater.idle()
