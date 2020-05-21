from config import TOKEN,DB_NAME
import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
from helpers import DBHelper
from PIL import Image, ImageDraw, ImageFont





db=DBHelper(DB_NAME)

STATE_REGION=1
STATE_CALENDAR=2
TODAY,TOMORROW,REGIONS,DUO=('⌛️Бугун', '⏳ Эртага', '🔄 Ҳудудни ўзгартириш', '🤲 Оғиз очиш,ёпиш дуоси')
user_region=dict()

main_buttons=ReplyKeyboardMarkup([
    [TODAY, TOMORROW],[REGIONS, DUO]
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
        update.message.reply_html('Ассалому алайкум ва роҳматуллоҳи ва барокатуҳ. \n \n '
                                  'Аллоҳ таоло Қуръони каримда шундай марҳамат қилган:\n'
                                  '«Аҳлингизни намоз (ўқиш)га буюринг ва (ўзингиз ҳам) унга (намозга) бардошли бўлинг!» (Тоҳа, 132).'
                                  ' \n \n Марҳамат керакли ҳудудни танланг!'
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
        region = db.getRegion(user_region[user_id])
        query.message.reply_html("Намоз вақтлари <b> {} </b> uchun, қуйидагилардан бирини танланг!".format(region['name']), reply_markup=main_buttons)
        return STATE_CALENDAR

    except Exception as e:
        print(e)


def today(update, context):
    try:
        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return  STATE_REGION
        region_id = user_region[user_id]
        region = db.getRegion(region_id)
        time = int(datetime.date.today().strftime("%d"))
        times = db.getDataByTime(region_id, time)
        image = Image.open('image.jpg')
        draw = ImageDraw.Draw(image)
        font_city = ImageFont.truetype("arial.ttf", 28)
        font = ImageFont.truetype("arial.ttf", 18)
        draw.text(xy=(500, 50), text="{} шаҳри".format(region['name']), fill=(57, 153, 82), font=font_city)
        draw.text(xy=(500, 120), text="Тонг(Саҳарлик):      {}".format(times['sahar']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 160), text="Қуёш:              {}".format(times['quyosh']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 200), text="Пешин:           {}".format(times['peshin']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 240), text="Аср:               {}".format(times['asr']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 280), text="Шом(Ифтор):     {}".format(times['shom']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 320), text="Ҳуфтон:         {}".format(times['xufton']), fill=(57, 153, 82), font=font)

        image.save('vaqt.jpg')
        text = '<b>{} </b> учун бугунги кун намоз вақтлари: \n \n<b>Тонг:   </b>{} \n' \
               '<b>Қуёш: </b> {} \n<b>Пешин: </b> {} \n<b>Аср: </b> {} \n<b>Шом: </b> {} \n<b>Ҳуфтон: </b>{}' \
            .format(region['name'], times['sahar'], times['quyosh'], times['peshin'], times['asr'], times['shom'],
                    times['xufton'])

        update.message.reply_photo(photo=open('vaqt.jpg', 'rb'), caption=text, parse_mode="HTML")

    except Exception as e:
        print(e)

def tomorrow(update, context):
    try:

        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return STATE_REGION
        region_id = user_region[user_id]
        region = db.getRegion(region_id)
        tomorrow= datetime.date.today() + datetime.timedelta(days=1)
        time=tomorrow.strftime("%d")
        times = db.getDataByTime(region_id, time)
        image = Image.open('image.jpg')
        draw = ImageDraw.Draw(image)
        font_city = ImageFont.truetype("arial.ttf", 28)
        font = ImageFont.truetype("arial.ttf", 18)
        draw.text(xy=(500, 50), text="{} шаҳри".format(region['name']), fill=(57, 153, 82), font=font_city)
        draw.text(xy=(500, 120), text="Тонг(Саҳарлик):            {}".format(times['sahar']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 160), text="Қуёш:           {}".format(times['quyosh']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 200), text="Пешин:        {}".format(times['peshin']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 240), text="Аср:             {}".format(times['asr']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 280), text="Шом(Ифторлик):            {}".format(times['shom']), fill=(57, 153, 82), font=font)
        draw.text(xy=(500, 320), text="Ҳуфтон:       {}".format(times['xufton']), fill=(57, 153, 82), font=font)

        image.save('vaqt.jpg')
        text = '<b>{} </b> учун эртанги кун намоз вақтлари: \n \n<b>Тонг:   </b>{} \n' \
               '<b>Қуёш: </b> {} \n<b>Пешин: </b> {} \n<b>Аср: </b> {} \n<b>Шом: </b> {} \n<b>Ҳуфтон: </b>{}' \
            .format(region['name'], times['sahar'], times['quyosh'], times['peshin'], times['asr'], times['shom'],
                    times['xufton'])

        update.message.reply_photo(photo=open('vaqt.jpg', 'rb'), caption=text, parse_mode="HTML")
    except Exception as e:
        print(e)

def duo(update, context):
    text='<b>Саҳарлик (оғиз ёпиш) дуоси:</b> \nНавайту ан асума совма шаҳри Рамазона минал фажри илал мағриби, холисан лиллаҳи таъала. \n\n' \
         '<b>Ифторлик (оғиз очиш) дуоси:</b> \nАллоҳумма лака сумту ва бика аманту ва аъалайка таваккалту ва ъала ризқика афтарту, фағфирли, йа Ғоффару, ма қоддамту вама аххорту.'
    update.message.reply_photo(photo=open('duo.jpg', 'rb'), caption=text, parse_mode="HTML")

def regions(update, context):
    buttons=region_buttons()
    update.message.reply_text('Керакли худудни танланг', reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_REGION


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
            STATE_REGION: [
                CallbackQueryHandler(inline_callback),
                MessageHandler(Filters.regex('^(' + TODAY + ')$'), today),
                MessageHandler(Filters.regex('^(' + TOMORROW + ')$'), tomorrow),
                MessageHandler(Filters.regex('^(' + REGIONS + ')$'), regions),
                MessageHandler(Filters.regex('^(' + DUO + ')$'), duo),
            ],

            STATE_CALENDAR: [
                MessageHandler(Filters.regex('^('+TODAY+')$'), today),
                MessageHandler(Filters.regex('^('+TOMORROW+')$'), tomorrow),
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