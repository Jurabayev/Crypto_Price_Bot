from auth_data import token
import requests
from datetime import datetime
import telebot
from telebot import types

def crypto_bahalar(crypto):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd'
    jogaby = requests.get(url)
    data=jogaby.json()

    shu_gun_senesi = datetime.now().strftime("%d.%m.%Y %H:%M")

    if crypto in data and "usd" in data[crypto]:
        return f"{crypto.capitalize()} bahasy: {data[crypto]['usd']}$\nSene: {shu_gun_senesi}"
    else:
        return "Bagyshlan kriptowalyutanyn bahasyny tapyp bimedim"


bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start_knopka(message):
    if message:

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        btc_knopka = types.InlineKeyboardButton("Bitcoin bahasy", callback_data="bitcoin")
        ltc_knopka = types.InlineKeyboardButton("Litecoin bahasy", callback_data="litecoin")
        eth_knopka = types.InlineKeyboardButton("Ethereum bahasy", callback_data="ethereum")

        keyboard.add(btc_knopka, ltc_knopka, eth_knopka)

        bot.send_message(message.chat.id, "Haysy kriptowalyutanyn bahasyny bilesiniz gelyar?", reply_markup=keyboard)

@bot.callback_query_handler(func = lambda call:True)
def knopka_basylanda_jogap(callback):
    if callback.message:

        bahasy = crypto_bahalar(callback.data)

        bot.send_message(callback.message.chat.id, f"{bahasy}")

        start_knopka(callback.message)

bot.polling()