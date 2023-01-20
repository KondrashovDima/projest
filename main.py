from telegram.ext import CallbackContext
from telegram.ext.updater import Updater
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from translate import Translator
from globals import lang, started, api_string
lang = ''
started = False
api_string = '5855320056:AAHAc2gcc8ATgLdK1SjqpuvA7LELk0AahZI'


def select_lang(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Арабский", callback_data='arabic'),
            InlineKeyboardButton("Немецкий", callback_data='german'),
            InlineKeyboardButton("Испанский", callback_data='spanish'),
        ],
        [
            InlineKeyboardButton("Французский", callback_data='french'),
            InlineKeyboardButton("Китайский", callback_data='chinese'),
            InlineKeyboardButton("Английский", callback_data='english')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Выберите язык для перевода:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext):
    global lang
    lang = update.callback_query.data.lower()
    query = update.callback_query
    query.answer()
    if query.data == 'english':
        string = 'Английский'
    if query.data == 'french':
        string = 'Французский'
    if query.data == 'german':
        string = 'Немецкий'
    if query.data == 'chinese':
        string = 'Китайский'
    if query.data == 'arabic':
        string = 'Арабский'
    if query.data == 'spanish':
        string = 'Испанский'
    query.edit_message_text(
        text=f'Слова будут переводиться с Русского на {string} язык!\nОтправьте сообщение, чтобы перевести его!')


def lang_translator(user_input):
    translator = Translator(from_lang='russian', to_lang=lang)
    translation = translator.translate(user_input)
    return translation


def reply(update: Update, context: CallbackContext):
    if not started:
        update.message.reply_text(
            'Для начала включите бота!\nДля этого введите команду /start.')
        return
    if lang == '':
        update.message.reply_text(
            'Сначала выберите язык для перевода!\nДля этого введите команду /select_language.')
        return
    user_input = update.message.text
    update.message.reply_text(lang_translator(user_input))


def sel_lang(update: Update, context: CallbackContext):
    global started
    if started:
        select_lang(update, context)
        return
    update.message.reply_text(
        'Для начала включите бота!\nДля этого введите команду /start.')


def start(update: Update, context: CallbackContext):
    global started
    if started:
        update.message.reply_text('Бот уже запущен!')
        return
    started = True
    update.message.reply_text(
        'Привет, я бот-переводчик. Я могу переводить слова с русского языка на английский, немецкий, французский, испанский, арабский и китайский. Чтобы выбрать язык для перевода введите команду /select_language.')


def run():
    API = api_string
    updater = Updater(API, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('select_language', sel_lang))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


run()