#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	context.user_data['objetivo_str'] = str(random.randrange(1000, 9999, 1))
	context.user_data['intentos'] = 8
	update.message.reply_text('Que comience el juego!')
	context.user_data['jugando'] = True
	
def stop(update,context):
	context.user_data['jugando'] = False
	update.message.reply_text("El juego se ha detenido. Loser.")
	

def help(update, context):
	"""Send a message when the command /help is issued."""
	update.message.reply_text('El juego consiste en adivinar un número de 4 cifras, del 1000 al 9999 en un máximo de 8 intentos. Te responderé con (C = una cifra existe y está en su sitio, v = una cifra existe, x = una cifra no pertenece a la solución)')
	update.message.reply_text('Si por ejemplo tienes que adivinar 5412 y escribes 4702 te responderé Cvxx. C por el 2, v por el 4, y xx por el 7 y el 0.')


def echo(update, context):
	"""Echo the user message."""
	if 'jugando' not in context.user_data:
		context.user_data['jugando'] = False
	if not context.user_data['jugando']:
		update.message.reply_text("Tienes que empezar una nueva partida. Reinicia el juego con /start")
		return
	if context.user_data['intentos'] < 1:
		update.message.reply_text("Qué vergüenza, no te quedan intentos... reinicia el juego con /start")
		return
	if len(update.message.text) is not 4:
		update.message.reply_text("Error, debe tener 4 caracteres.")
		return
	respuesta = probar_numero(update.message.text,context.user_data['objetivo_str'])
	if respuesta == "fin":
		context.user_data['jugando'] = False
		update.message.reply_text("Enhorabuena campeón! Ahora vas y se lo cuentas a alguien.")		
		return
	else: 
		update.message.reply_text(respuesta)
	context.user_data['intentos'] = context.user_data['intentos']-1
	update.message.reply_text("Te quedan "+str(context.user_data['intentos'])+" intentos.")
	


def probar_numero(numero,solucion):

	a = get_numero_posicion(numero,1)
	b = get_numero_posicion(numero,2)
	c = get_numero_posicion(numero,3)
	d = get_numero_posicion(numero,4)
	
	respuesta = []
	for x in range(1,5):
		respuesta.append(comprobar(numero,x,solucion))
	respuesta.sort()
	respuesta = "".join(respuesta)
	if respuesta == "CCCC":
		respuesta = "fin"
	return  respuesta
	
def comprobar(numero,posicion,solucion):	
	if get_numero_posicion(numero,posicion) == get_numero_posicion(solucion,posicion):
		return ("C")
	elif get_numero_posicion(numero,posicion) in solucion:
		return ("v")
	else:
		return("x")
	
def get_numero_posicion(numero,posicion):
	if posicion == 1:
		return numero[:-3]
	elif posicion == 2:
		return  numero[1:-2]
	elif posicion == 3:
		return  numero[2:-1]
	elif posicion == 4:
		return  numero[3:]


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(TELE_KEY, use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("stop", stop))
	dp.add_handler(CommandHandler("help", help))

	# on noncommand i.e message - echo the message on Telegram
	dp.add_handler(MessageHandler(Filters.text, echo))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
