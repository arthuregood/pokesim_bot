import pokepy
import random
import telegram
import time
import logging
from datetime import datetime
import mysql.connector
from mysql.connector import MySQLConnection, Error


token = '952409205:AAHSVni5FVXtKTOc-8nT8dh5yhq77Jej1as'
client = pokepy.V2Client()
bot = telegram.Bot(token=token)


def Captura(update, context):

    random_pokemon = range(1, 387)
    answer = [
        'Droga, foi tão perto!',
        'Você errou a pokebola!',
        'O Pokemon fugiu!'
    ]

    chat_id = update.effective_chat.id
    user = update.message.from_user
    now = datetime.now()
    pokemon = client.get_pokemon(random.choice(random_pokemon))
    catch = client.get_pokemon_species(pokemon.id)
    chance = False
    isShiny = False
    shinyChance = random.choice(range(0, 99))

    if shinyChance != 0:
        bot.sendAnimation(
            chat_id, animation=open(f'sprites/normal/{pokemon.name.capitalize()}.gif', 'rb'), caption=f'Você encontrou um {pokemon.name.capitalize()}. Pokebola, vai!')

    else:
        isShiny = True
        bot.sendAnimation(
            chat_id, animation=open(f'sprites/shiny/{pokemon.name.capitalize()}.gif', 'rb'), caption=f'Você encontrou um {pokemon.name.capitalize()} Shiny! Pokebola, vai!')

    bot.sendAnimation(
        chat_id, animation=open('sprites/pokeball.mp4', 'rb'))
    time.sleep(3)

    i = 10
    r = 0
    n = 0

    # method to determine capture chance
    while r <= 16:
        num = random.choice(range(0, 99))
        if catch.capture_rate < n:
            if num < i:
                chance = True
                break
            else:
                break
        i += 5
        n += 16
        r += 1

    if chance == True:

        if isShiny == True:
            update.message.reply_text(
                f'Parabéns, você capturou um {pokemon.name.capitalize()} Shiny!')
        else:
            update.message.reply_text(
                f'Parabéns, você capturou um {pokemon.name.capitalize()}!')
        insertPokemonDB(update, pokemon, isShiny, now, context)

    else:
        update.message.reply_text(random.choice(answer))


def checkPokedex(update, context):

    value = (update.message.text)
    chat_id = update.effective_chat.id
    legendary_ids = [144, 145, 146, 150, 151, 243, 244, 245, 249,
                     250, 251, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386]

    if value == '/pokedex' or value == '/pokedex@pokesim_bot':
        bot.sendAnimation(
            chat_id, animation=open('sprites/pokedex.gif', 'rb'), caption='Uma pequena enciclopédia de Pokemons! Tente colocar o nome ou número de um Pokemon depois de "/pokedex"')

    else:
        value = value.replace('/pokedex@pokesim_bot ', '').lower()
        value = value.replace('/pokedex ', '').lower()
        try:
            pokemon = client.get_pokemon(value)

            if pokemon.id in legendary_ids:
                bot.sendAnimation(
                    chat_id, animation=open(f'sprites/normal/{pokemon.name.capitalize()}.gif', 'rb'), caption=f'''
                        Pokemon Lendário!\nNúmero - {pokemon.id}\nNome - {pokemon.name.capitalize()}\nPeso - {pokemon.weight/10} kg\nTamanho - {pokemon.height/10} m\n
                        ''')
            else:
                bot.sendAnimation(
                    chat_id, animation=open(f'sprites/normal/{pokemon.name.capitalize()}.gif', 'rb'), caption=f'''
                        Número - {pokemon.id}\nNome - {pokemon.name.capitalize()}\nPeso - {pokemon.weight/10} kg\nTamanho - {pokemon.height/10} m
                        ''')

        except:
            bot.sendAnimation(
                chat_id, animation=open('sprites/missingno.gif', 'rb'), caption='Missingno! Insira um pokémon válido!')


def startLogging(update, context):

    user = update.message.from_user
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    log = open("logStart.txt", "a+")
    log.write(
        f"{current_time} - User: {user.first_name} ({user.id}) - Language: {user.language_code}\n")
    log.close()


def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='pokemon',
                                       user='root',
                                       password='my-secret-pw')
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def insertPokemonDB(update, pokemon, isShiny, now, context):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    conn = mysql.connector.connect(host='localhost',
                                   database='pokemon',
                                   user='root',
                                   password='my-secret-pw')

    user = update.message.from_user
    mycursor = conn.cursor()

    sql = "INSERT INTO captured (id, pokemon_name, is_shiny, date) VALUES (%s, %s, %s, %s)"
    val = [user.id, pokemon.name.capitalize(), isShiny, now]

    log = open("logCapture.txt", "a+")
    log.write(
        f"{current_time} - User: {user.first_name} ({user.id}) - Pokemon: {pokemon.name.capitalize()} - Shiny: {isShiny}\n")
    log.close()

    mycursor.execute(sql, val)
    conn.commit()
    print(mycursor.rowcount, "record inserted.")
