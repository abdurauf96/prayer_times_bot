from config import TOKEN,DB_NAME
from datetime import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
from helpers import DBHelper


db=DBHelper(DB_NAME)

STATE_REGION=1
STATE_CALENDAR=2
TODAY,TOMORROW,MONTH,REGIONS,DUO=('Bugun', 'Ertaga', 'To\'liq taqvim', 'Xududlar', 'Duo')
user_region=dict()

main_buttons=ReplyKeyboardMarkup([
    [TODAY, TOMORROW, MONTH ], [REGIONS, DUO]
], resize_keyboard=True)


def region_buttons():
    regions = db.regions()
    br = []
    buttons = []

    for region in regions:
        br.append(InlineKeyboardButton(region['name'], callback_data=str(region['key_id'])))
        if len(br) == 2:
            buttons.append(br)
            br = []
    return buttons



def start(update, context):
    try:
        buttons=region_buttons()
        user = update.message.from_user
        user_region[user.id]=None
        update.message.reply_html('Assalomu alaykum <b>{}</b> \n \n Ramazon oyi muborak bolsin! \n \n Marhamat o\'zingizga kerakli xududni tanlang!'
                                  .format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")
        return STATE_REGION
    except Exception as e:
        print(e)

def inline_callback(update, context):

    try:
        query=update.callback_query
        user_id=query.from_user.id
        user_region[user_id]=int(query.data)
        query.message.delete()
        query.message.reply_text("Ramazon taqvimi 2020!", reply_markup=main_buttons)
        return STATE_CALENDAR

    except Exception as e:
        print(e)


def today(update, context):
    try:
        user_id = update.message.from_user.id
        region_id = user_region[user_id]
        region = db.getRegion(region_id)
        time = int(datetime.today().strftime("%d"))
        times = db.getDataByTime(region_id, time)
        update.message.reply_html("<b>{} </b>viloyati uchun bugungi namoz vaqtlari: \n \n"
                                  "<b>Tong: </b> {} \n"
                                  "<b>Quyosh: </b> {} \n"
                                  "<b>Peshin: </b> {} \n"
                                  "<b>Asr: </b> {} \n"
                                  "<b>SHom: </b> {} \n"
                                  "<b>Xufton: </b> {} \n".format(region['name'], times['sahar'], times['quyosh'], times['peshin'],times['asr'],times['shom'],times['xufton']))

    except Exception as e:
        print(e)

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