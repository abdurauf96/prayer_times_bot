from config import TOKEN
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
from functions import getRegions

STATE_REGION=1
STATE_CALENDAR=2
TODAY,TOMORROW,MONTH,REGIONS,DUO=('Bugun', 'Ertaga', 'To\'liq taqvim', 'Xududlar', 'Duo')

main_buttons=ReplyKeyboardMarkup([
    [TODAY, TOMORROW, MONTH ], [REGIONS, DUO]
], resize_keyboard=True)


def start(update, context):
    buttons = [
        [
            InlineKeyboardButton('Farg\'ona', callback_data='reg1'),
            InlineKeyboardButton('Andijon', callback_data='reg2')
        ]
    ]
    user=update.message.from_user
    update.message.reply_html('Assalomu alaykum <b>{}</b> \n \n Ramazon oyi muborak bolsin! \n \n Marhamat o\'zingizga kerakli xududni tanlang!'
                              .format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons))

    return STATE_REGION

def inline_callback(update, context):
    query=update.callback_query
    query.message.delete()
    query.message.reply_text("Ramazon taqvimi 2020!", reply_markup=main_buttons)
    return STATE_CALENDAR

def today(update, context):
    update.message.reply_text('today')

def tomorrow(update, context):
    update.message.reply_text('tomorrow')

def month(update, context):
    update.message.reply_text('month')

def regions(update, context):
    update.message.reply_text('xududni tanlang')

def duo(update, context):
    update.message.reply_text('duo')

def main():
    #updater
    updater=Updater(TOKEN, use_context=True)

    #dispetcher
    dp=updater.dispatcher

    #dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(CallbackQueryHandler(inline_callback))

    conv_handler=ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_REGION: [CallbackQueryHandler(inline_callback)],
            STATE_CALENDAR: [
                MessageHandler(Filters.regex('^('+TODAY+')$'), today),
                MessageHandler(Filters.regex('^('+TOMORROW+')$'), tomorrow),
                MessageHandler(Filters.regex('^('+MONTH+')$'), month),
                MessageHandler(Filters.regex('^('+REGIONS+')$'), regions),
                MessageHandler(Filters.regex('^('+DUO+')$'), duo),
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

main()