import pokepy
import logging
import random
import telegram
import time
from telegram.ext import Updater, CommandHandler
from functions import Captura, doLogging, checkPokedex

client = pokepy.V2Client(cache='in_disk')
bot = telegram.Bot(token='')


# Enable logging
logging.basicConfig(
    format='%(asctime)s -  %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):

    doLogging(update, context)
    chat_id = update.effective_chat.id
    bot.sendPhoto(
        chat_id, photo=open('sprites/oak.png', 'rb'))
    update.message.reply_text('''
        Olá, bem-vindo ao mundo de Pokemon!\nEu sou o Professor Carvalho!
        \nEste mundo é habitado por criaturas chamadas Pokemon!\nPara alguns, eles são pets. Outros os usam em batalhas.\nEu... Bom, eu os estudo como profissão.
        ''')
    time.sleep(4)
    update.message.reply_text(
        'Envie /procurar para começar sua jornada Pokemon!')


def procurar(update, context):
    if random.choice(range(0, 99)) < 90:
        Captura(update, context)

    else:
        update.message.reply_text('Você não encontrou nenhum Pokemon.')


def pokedex(update, context):

    checkPokedex(update, context)


# Start bot
def main():
    updater = Updater(
        '', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('procurar', procurar))
    dp.add_handler(CommandHandler('pokedex', pokedex))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
