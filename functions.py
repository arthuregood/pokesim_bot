import pokepy
import random
import telegram
import time
import logging
from datetime import datetime

client = pokepy.V2Client(cache='in_disk')
bot = telegram.Bot(token='')


def Captura(update, context):

    random_pokemon = range(1, 387)
    answer = [
        'Droga, foi tão perto!',
        'Você errou a pokebola!',
        'O Pokemon fugiu!'
    ]

    chat_id = update.effective_chat.id
    pokemon = client.get_pokemon(random.choice(random_pokemon))
    catch = client.get_pokemon_species(pokemon.id)
    chance = False
    isShiny = False
    shinyChance = random.choice(range(0, 99))

    if shinyChance != 0:
        bot.sendAnimation(
            chat_id, animation=open(f'sprites/normal/{pokemon.name.capitalize()}.gif', 'rb'))
        update.message.reply_text(
            f'Você encontrou um {pokemon.name.capitalize()}. Pokebola, vai!')

    else:
        isShiny = True
        bot.sendAnimation(
            chat_id, animation=open(f'sprites/shiny/{pokemon.name.capitalize()}.gif', 'rb'))
        update.message.reply_text(
            f'Você encontrou um {pokemon.name.capitalize()} Shiny! Pokebola, vai!')

    bot.sendAnimation(
        chat_id, animation=open('sprites/pokeball.mp4', 'rb'))

    for i in range(3):
        time.sleep(1)
        update.message.reply_text('.')
    time.sleep(1)

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
        captureLog(update, pokemon, isShiny, context)

    else:
        update.message.reply_text(random.choice(answer))


def checkPokedex(update, context):

    value = (update.message.text)
    chat_id = update.effective_chat.id

    if value == '/pokedex' or value == '/pokedex@pokesim_bot':
        bot.sendAnimation(
            chat_id, animation=open('sprites/pokedex.gif', 'rb'))
        update.message.reply_text(
            'Uma pequena enciclopédia de Pokemons! Tente colocar o nome ou número de um Pokemon depois de "/pokedex"')

    else:
        value = value.replace('/pokedex@pokesim_bot ', '').lower()
        value = value.replace('/pokedex ', '').lower()

        try:
            pokemon = client.get_pokemon(value)
            bot.sendAnimation(
                chat_id, animation=open(f'sprites/normal/{pokemon.name.capitalize()}.gif', 'rb'))
            update.message.reply_text(f'''
                Número - {pokemon.id}\nNome - {pokemon.name.capitalize()}\nPeso - {pokemon.weight/10} kg\nTamanho - {pokemon.height/10} m
                ''')

        except:
            bot.sendAnimation(
                chat_id, animation=open('sprites/missingno.gif', 'rb'))
            update.message.reply_text('Insira um pokémon válido!')


def doLogging(update, context):

    user = update.message.from_user
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    log = open("logStart.txt", "a+")
    log.write(
        f"{current_time} - User: {user.first_name} ({user.id}) - Language: {user.language_code}\n")
    log.close()


def captureLog(update, pokemon, isShiny, context):

    user = update.message.from_user
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    log = open("logCapture.txt", "a+")
    log.write(
        f"{current_time} - User: {user.first_name} - Pokemon: {pokemon.name.capitalize()} - Shiny: {isShiny}\n")
    log.close()
