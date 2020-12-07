import pokepy
import logging
import random
import telegram
import time
from telegram.ext import Updater, CommandHandler
from functions import Captura, startLogging, checkPokedex, connect
import mysql.connector
from mysql.connector import MySQLConnection, Error

token = ''
client = pokepy.V2Client()
bot = telegram.Bot(token=token)


# Enable logging
logging.basicConfig(
    format='%(asctime)s -  %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):

    startLogging(update, context)
    chat_id = update.effective_chat.id
    bot.sendPhoto(
        chat_id, photo=open('assets/oak.png', 'rb'), caption='''Olá, bem-vindo ao mundo de Pokemon!\nEu sou o Professor Carvalho!
        \nEste mundo é habitado por criaturas chamadas Pokemon!\nPara alguns, eles são pets. Outros os usam em batalhas.\nEu... Bom, eu os estudo como profissão.
        ''')
    time.sleep(3)
    update.message.reply_text(
        'Envie / para começar sua jornada Pokemon!')


def procurar(update, context):
    if random.choice(range(0, 99)) < 90:
        Captura(update, context)

    else:
        update.message.reply_text('Você não encontrou nenhum Pokemon.')


def pokedex(update, context):
    checkPokedex(update, context)


def returnPokemon(update, context):
    try:
        user = update.message.from_user
        conn = mysql.connector.connect(host='localhost',
                                       database='pokemon',
                                       user='root',
                                       password='my-secret-pw')
        mycursor = conn.cursor()
        mycursor.execute(
            f"SELECT pokemon_name, is_shiny from captured where id = {user.id}")
        row = mycursor.fetchone()
        pokemons = []
        captured = 'Segundo sua Pokedex, você já capturou: '

        while row is not None:
            pokemons.append(row)
            row = mycursor.fetchone()

        pokemon_name, is_shiny = map(list, zip(*pokemons))
        i = 0
        for value in is_shiny:
            if value == 0:
                captured = captured + f'\n> {pokemon_name[i]}'
            else:
                captured = captured + f'\n> {pokemon_name[i]} Shiny'
            i += 1

        update.message.reply_text(f'{captured}')
    except:
        update.message.reply_text(
            'Não há dados o suficiente sobre seus Pokemons!')

# Start bot


def main():
    updater = Updater(
        token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('procurar', procurar))
    dp.add_handler(CommandHandler('pokedex', pokedex))
    dp.add_handler(CommandHandler('capturados', returnPokemon))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    connect()
    main()
